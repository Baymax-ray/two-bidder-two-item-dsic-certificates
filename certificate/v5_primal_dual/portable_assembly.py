"""Exact V5 assembly, deliberately separate from workspace preservation.

This does not import or monkeypatch phase_ledger.py. Its numeric claims are
rederived with Fraction and checked against the unchanged recorded phase.
The canceled first-event certificate is used only for an accounting identity;
its mathematical theorem is unnecessary for the reduced upper formula.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path, PureWindowsPath
import json
import sys

def require(condition,message):
    if not condition:
        raise RuntimeError(message)

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def rounded(value,up=False):
    scaled=value*10**30
    integer=-((-scaled.numerator)//scaled.denominator) if up else scaled.numerator//scaled.denominator
    sign='-' if integer<0 else ''
    integer=abs(integer)
    return f'{sign}{integer//10**30}.{integer%10**30:030d}'

def interval(lower,upper):
    require(lower<=upper,'reversed interval')
    return {'lower':str(lower),'upper':str(upper),'decimal_enclosure':[rounded(lower),rounded(upper,True)]}

def calculate(auction):
    phase=read(auction/'V5_gap_closure/certificate/phase_ledger.json')
    primal=read(auction/'V5_gap_closure/certificate/primal_global.json')
    independent=read(auction/'V5_gap_closure/certificate/primal_independent.json')
    faces=read(auction/'V5_gap_closure/certificate/primal_face_integrals.json')
    support=read(auction/'V5_gap_closure/certificate/global_duality.json')
    bb=read(auction/'V5_gap_closure/certificate/bb_global.json')
    remainder=read(auction/'V4_6_3_slack_atlas/certificate/numerical_remainder.json')
    master=read(auction/'V4_8A_frozen_primal/certificate/master_certificate.json')
    master_independent=read(auction/'V4_8A_frozen_primal/certificate/master_independent.json')
    retained=read(auction/'V4_6_2_upper/certificate/upper_ledger.json')
    event=read(auction/'V4_8A_frozen_primal/certificate/first_event_gain.json')
    old=read(auction/'V4_8B_support_redesign/certificate/phase_ledger.json')
    require(all('PASS' in data['status'] for data in (phase,primal,independent,faces,support,bb,remainder,master,master_independent,retained,old)),'non-PASS source record')
    require(remainder['settings']['depth_B']==20 and remainder['settings']['depth_D']==20 and remainder['settings']['depth_averaged']==26,'wrong remainder settings')
    upper0=F(retained['final_upper'])
    require(upper0==F(retained['anchor_upper'])-F(retained['exact_common_support_subtraction'])-F(retained['exact_sparse_cycle_subtraction']),'retained upper assembly differs')
    E=F(remainder['total_E']['lower'])
    G=F(master['exact_total_gain_lower'])
    require(G==F(master_independent['exact_total_gain_lower']),'master disagreement')
    splice=F(support['global_gain_lower']);BB=F(bb['exact_upper_decrease'])
    require(E>0 and G>0 and splice>0 and BB>0,'nonpositive accepted deduction')
    upper=upper0-E-G-splice-BB
    oldupper=F(old['preserved_exact_upper']);giveback=F(event['gain_interval'][0])
    require(oldupper+giveback==upper0-E-G,'first-event cancellation identity differs')
    require(upper==oldupper+giveback-splice-BB,'legacy and reduced V5 assemblies differ')
    lower,high=map(F,primal['ledger']['revenue_enclosure'])
    require([lower,high]==list(map(F,independent['independent_revenue_enclosure'])),'primal independent disagreement')
    oldlow,oldhigh=map(F,faces['moment_enclosures']['R4'])
    require(lower-oldhigh>F(3,62500) and high<upper,'strict gain/gap claim fails')
    oldgap=(oldupper-oldhigh,oldupper-oldlow)
    newgap=(upper-high,upper-lower)
    reduction=(oldgap[0]-newgap[1],oldgap[1]-newgap[0])
    derived={
        'new_revenue':interval(lower,high),'new_exact_upper':str(upper),'new_upper':interval(upper,upper),
        'remaining_gap':interval(*newgap),'old_gap':interval(*oldgap),'gap_reduction':interval(*reduction),
        'gap_reduction_percent':interval(100*reduction[0]/oldgap[1],100*reduction[1]/oldgap[0]),
        'primal_gain':interval(lower-oldhigh,high-oldlow),'net_upper_decrease':interval(oldupper-upper,oldupper-upper),
    }
    for key,value in derived.items():
        require(phase[key]==value,'recorded V5 numeric assembly differs: '+key)
    for name,digest in phase['source_hashes'].items():
        path=Path(name);windows=PureWindowsPath(name)
        require(name and not windows.drive and not windows.root
                and not path.is_absolute() and '..' not in path.parts,
                'unsafe phase source path')
        resolved=(auction/path).resolve()
        require(resolved!=auction and resolved.is_relative_to(auction),
                'phase source escapes auction')
        require(sha256(resolved.read_bytes()).hexdigest()==digest,'phase input identity differs: '+name)
    require(lower/upper>F(993382,1000000),'99.3382 percent guarantee fails')
    require(phase['unrestricted_optimum']=='OPEN','unsupported optimum claim')
    return {'status':'PORTABLE_V5_EXACT_ASSEMBLY_PASS',**derived,
            'upper_formula':'U_V462 - E_lower - G_master - G_splice - G_BB',
            'ratio_guarantee':'0.993382','guarantee_percent':'99.3382',
            'workspace_preservation':'Not replayed by this portable assembly; the original 4278-file claim remains historical workspace evidence.',
            'unrestricted_optimum':'OPEN'}

if __name__=='__main__':
    require(sys.flags.optimize==0 and len(sys.argv)==2,'Run without optimization: assembly AUCTION')
    result=calculate(Path(sys.argv[1]).resolve())
    print(result['status'])
    print('LOWER_ENCLOSURE',*result['new_revenue']['decimal_enclosure'])
    print('UPPER_ENCLOSURE',*result['new_upper']['decimal_enclosure'])
    print('GAP_ENCLOSURE',*result['remaining_gap']['decimal_enclosure'])
    print('GUARANTEE_GT_99_3382_PERCENT_PASS OPTIMUM_OPEN')
