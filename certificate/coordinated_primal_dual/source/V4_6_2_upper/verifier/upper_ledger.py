"""Exact decreasing unrestricted-upper ledger and certificate compatibility."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
OLD=F(3715139591287203,4194304000000000)

def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def decimal(q,digits=22,up=False):
    den=10**digits;v=q*den
    n=-((-v).numerator//(-v).denominator) if up else v.numerator//v.denominator
    s=str(abs(n)).zfill(digits+1)
    return ('-' if n<0 else '')+s[:-digits]+'.'+s[-digits:]

def verify():
    flow=read('flow_majorant_certificate.json');ind=read('certificate/independent_majorant.json')
    assert flow['amplitude']==ind['amplitude']=='1'
    assert sha256((ROOT/'flow_majorant_certificate.json').read_bytes()).hexdigest()==ind['primary_certificate_sha256']
    assert [r['upper_bound'] for r in flow['results']]==[r['upper_bound'] for r in ind['results']]
    sign=read('flow_sign_43_certificate.json')
    assert sign['w_square']==['0','43/100']
    assert all(r['max_upper_control']<0 and r['coverage']=='1' for r in sign['records'])
    local=read('certificate/conditional_global_splice.json')
    assert local['W_area']=='1849/10000' and local['bidder_symmetry_factor']==2
    assert local['support_zero_on_W_overlap']
    cyc=read('certificate/sparse_cycle.json')
    gain=F(cyc['exact_strict_upper_reduction'])
    assert gain==F(81,10000000000)
    assert len(cyc['pairwise_separations'])==28
    # The field coefficients must be identical across all three operations.
    archive=ROOT.parents[3]/'research/closed/two-bidder-two-item-dsic-certificates/certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound'
    manifest=json.loads((archive/'manifest.json').read_text(encoding='utf-8'))
    digest=sha256((archive/'manifest.json').read_bytes()).hexdigest()
    assert digest==flow['dependencies']['manifest.json']==cyc['source_manifest_sha256']
    assert manifest['theta']==local['old_manifest_theta']
    rows=[dict(stage='inherited upper',upper=str(OLD))]
    for r in flow['results']:rows.append(dict(stage='continuous majorant depth '+str(r['depth']),upper=r['upper_bound']))
    anchor=F(rows[-1]['upper'])
    for r in local['sequence']:
        rows.append(dict(stage='common support radial integral partition '+str(r['radial_partition']),upper=str(anchor-F(r['delta']))))
    delta=F(local['sequence'][-1]['delta'])
    for density,reduction in zip(cyc['certified_density_sequence'],cyc['exact_reduction_sequence']):
        rows.append(dict(stage='long-range cycle density '+density,upper=str(anchor-delta-F(reduction))))
    assert all(F(a['upper'])>F(b['upper']) for a,b in zip(rows,rows[1:]))
    for r in rows:r['decimal_upper_enclosure']=decimal(F(r['upper']),22,True)
    final=F(rows[-1]['upper'])
    safe=F(decimal(final,12,True))
    lowerdata=json.loads((ROOT.parent/'V4_6/certificate/consolidated_bounds.json').read_text(encoding='utf-8'))
    lo,hi=map(F,lowerdata['revenue_rational_interval'])
    assert hi<final<OLD
    data=dict(status='V4_6_2_GLOBAL_UPPER_SEQUENCE_PASS_GAP_OPEN',
        exact_upper_expression='U_majorant_depth20 - Delta_common_support_1024 - 81/10000000000',
        anchor_upper=str(anchor),exact_common_support_subtraction=str(delta),exact_sparse_cycle_subtraction=str(gain),
        final_upper=str(final),simple_rational_upper=str(safe),simple_decimal_upper=decimal(safe,12),
        final_upper_decimal_enclosure=[decimal(final),decimal(final,22,True)],
        improvement_over_inherited_decimal_enclosure=[decimal(OLD-final),decimal(OLD-final,22,True)],
        unchanged_lower_mechanism='V4_6/verifier/price_joint_reallocation.py',
        lower_revenue_decimal_enclosure=lowerdata['revenue_decimal_enclosure'],
        remaining_gap_decimal_enclosure=[decimal(final-hi),decimal(final-lo,22,True)],
        decreasing_sequence=rows,
        global_certificate='common nonnegative capacity density Pi prime; H1(Pi prime)=H2(Pi prime)=0 over full randomized DSIC/IR',
        independent_checks=['full 1351220-node continuous majorant replay','symbolic conditional integral and allocation-region audit','whole-box sparse-cycle numerator and symmetry audit'],
        equality_status='not matching V4.6; positive-volume lottery flatness still fails in unchanged regions',
        no_claims=['optimal revenue','uniqueness of an equality mechanism','attainment or nonattainment','finite type-grid mechanism optimality'])
    path=ROOT/'certificate/upper_ledger.json'
    if '--write' in sys.argv:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(path.read_text(encoding='utf-8'))==data
    print(data['status']);print('safe_upper',data['simple_decimal_upper']);print('final_enclosure',data['final_upper_decimal_enclosure']);print('remaining_gap',data['remaining_gap_decimal_enclosure']);print('strictly_decreasing_bounds',len(rows))
    return data
if __name__=='__main__':verify()
