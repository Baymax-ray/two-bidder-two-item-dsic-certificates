# Exact V5 global lower/upper assembly with explicit give-back accounting.
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1];AUCTION=ROOT.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def decimal(q,up=False,digits=30):
    scale=10**digits;n=-((-q*scale).__floor__()) if up else (q*scale).__floor__()
    sign='-' if n<0 else '';a,b=divmod(abs(n),scale)
    return f'{sign}{a}.{b:0{digits}d}'
def interval(lo,hi):
    assert lo<=hi
    return dict(lower=str(lo),upper=str(hi),decimal_enclosure=[decimal(lo),decimal(hi,True)])
def preservation():
    count=0
    base=Path(chr(92)*2+'?'+chr(92)+str(AUCTION)) if sys.platform=='win32' else AUCTION
    for line in (ROOT/'certificate/baseline_SHA256SUMS').read_text().splitlines():
        digest,rel=line.split('  ',1)
        assert rel!='CURRENT_PHASE.md' and not rel.startswith('V5_gap_closure/')
        assert sha256((base/rel).read_bytes()).hexdigest()==digest,rel
        count+=1
    assert count==4278
    return count
def calculate():
    files={'old':'V4_8B_support_redesign/certificate/phase_ledger.json',
           'event':'V4_8A_frozen_primal/certificate/first_event_gain.json',
           'primal':'V5_gap_closure/certificate/primal_global.json',
           'faces':'V5_gap_closure/certificate/primal_face_integrals.json',
           'primal_independent':'V5_gap_closure/certificate/primal_independent.json',
           'splice':'V5_gap_closure/certificate/global_duality.json',
           'BB':'V5_gap_closure/certificate/bb_global.json'}
    data={k:read(AUCTION/p) for k,p in files.items()}
    assert all('PASS' in data[k]['status'] for k in ['primal','faces','primal_independent','splice','BB'])
    old=data['old'];uold=F(old['preserved_exact_upper'])
    giveback=F(data['event']['gain_interval'][0])
    splice=F(data['splice']['global_gain_lower']);bb=F(data['BB']['exact_upper_decrease'])
    unew=uold+giveback-splice-bb
    assert giveback<splice and unew<uold
    lower,hi=map(F,data['primal']['ledger']['revenue_enclosure'])
    independent=list(map(F,data['primal_independent']['independent_revenue_enclosure']))
    assert independent==[lower,hi]
    oldlo,oldhi=map(F,data['faces']['moment_enclosures']['R4'])
    assert lower-oldhi>F(3,62500)
    assert hi<unew
    oldgap=[uold-oldhi,uold-oldlo];newgap=[unew-hi,unew-lower]
    reduction=[oldgap[0]-newgap[1],oldgap[1]-newgap[0]]
    percent=interval(100*reduction[0]/oldgap[1],100*reduction[1]/oldgap[0])
    assert F(percent['lower'])>F(78,10)
    hashes={p:sha256((AUCTION/p).read_bytes()).hexdigest() for p in files.values()}
    for name in ['global_duality','bb_global','primal_face_integrals','primal_global','primal_independent']:
        p=ROOT/'verifier'/f'{name}.py';hashes[str(p.relative_to(AUCTION)).replace(chr(92),'/')]=sha256(p.read_bytes()).hexdigest()
    return dict(status='V5_TWO_SIDED_GLOBAL_GAP_REDUCTION_PASS_OPTIMUM_OPEN',
        preserved_predecessor_files=preservation(),new_complete_mechanism='verifier/primal_global.py, tau=1/100',
        new_revenue=interval(lower,hi),new_exact_upper=str(unew),new_upper=interval(unew,unew),
        remaining_gap=interval(*newgap),old_gap=interval(*oldgap),gap_reduction=interval(*reduction),
        gap_reduction_percent=percent,primal_gain=interval(lower-oldhi,hi-oldlo),
        net_upper_decrease=interval(uold-unew,uold-unew),
        exact_upper_formula='U_V48B + G_V48A_first_event_lower - G_global_splice_lower - G_BB_exact',
        upper_components=dict(inherited_exact_upper=str(uold),give_back_entire_first_event_lower=str(giveback),
            global_splice_lower=str(splice),BB_exact_gain=str(bb),
            inherited_retained='V4.6.2 sparse flow, W conditional support, contracted integration remainder, and V4.8A BB master.',
            inherited_removed='All V4.8A first-event fields; the entire old deduction is given back before the new splice.',
            excluded='Overlapping QQ curl candidate is not accepted and is not subtracted.'),
        common_regional_ledger=dict(
            added_support='W union J union item_swap(J), J=(43/100,1/2] x [0,7/20]; QQ and mixed profiles.',
            global_splice='Gain lower is the net complete common-capacity mass decrease, including positive opposing-price excess and all overlaps.',
            BB=data['BB']['regional_ledger'],
            primal='The degree-five pushforward identity integrates every induced ownership, sale, lottery and rent change.',
            new_primal_screening_source='0 on every W/J conditional slice: T(w)<=w stays free SJA and T(v)<=v leaves D0 at zero utility.',
            origin_IR='0 for the new mechanism.',
            full_gap_identity='U5-R_tau=C5(tau)+V5(tau)+K_retained(tau)+K_BB(tau)+E5, all nonnegative; K_retained includes inherited continuous PSD convexity and finite IC terms.',
            numerical_boundary='The old incumbent numerical atlas components are not relabeled as new-primal components. C,V,K remain defined by the complete new support; their sum plus enclosure E is bounded by the exact remaining-gap interval.'),
        decisive_outcomes=['Materially stronger complete pointwise DSIC/IR mechanism','Materially smaller unrestricted randomized-DSIC upper bound'],
        unrestricted_optimum='OPEN',matching_certificate='NOT_ESTABLISHED',
        source_hashes=hashes)
if __name__=='__main__':
    out=calculate();p=ROOT/'certificate/phase_ledger.json'
    if '--write' in sys.argv:p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert read(p)==out
    print(out['status'])
    for k in ['new_revenue','new_upper','remaining_gap','gap_reduction_percent','net_upper_decrease']:
        print(k,out[k]['decimal_enclosure'])
