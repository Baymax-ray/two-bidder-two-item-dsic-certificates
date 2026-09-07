# Independent exact Fraction replay of the full BB translated-flow gain.
from pathlib import Path
from fractions import Fraction as F
from math import comb,prod
from itertools import product
from hashlib import sha256
import importlib.util,json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Run without -O.')
ROOT=Path(__file__).resolve().parents[1]
AUCTION=ROOT.parent
SOURCE=AUCTION/'V4_6_3_slack_atlas/verifier/independent_lifted_fields.py'
spec=importlib.util.spec_from_file_location('independent_source_coefficients',SOURCE)
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
CORR,manifest=source.corrections()
MENU_SOURCE=AUCTION/'V4_6_3_slack_atlas/verifier/independent_menu_classifier.py'
spec=importlib.util.spec_from_file_location('incumbent_menu_intervals',MENU_SOURCE)
menus=importlib.util.module_from_spec(spec);spec.loader.exec_module(menus)
ZERO=(0,0,0,0)
C=[tuple(map(F,['23/40','3/5','91/100','13/40'])),tuple(map(F,['29/40','23/40','91/100','13/40']))]
H=tuple(map(F,['3/40','3/20','9/100','13/40']))
VOLUME=prod(2*h for h in H)
SHIFT=(F(3,20),-F(1,40))
def normalize(poly,center):
    out={}
    for e,c in poly.items():
        for k in product(*(range(n+1) for n in e)):
            co=c*prod(F(comb(n,j))*x**(n-j)*h**j for n,j,x,h in zip(e,k,center,H))
            out[k]=out.get(k,F())+co
    return {k:c for k,c in out.items() if c}
P=[]
for center in C:
    raw=[CORR[0],CORR[1]]+[{(e[2],e[3],e[0],e[1]):c for e,c in p.items()} for p in CORR]
    P.append([normalize(p,center) for p in raw])
HESS=[[[[sum((abs(c)*e[j]*(e[k]-(j==k)) for e,c in p.items() if e[j] and e[k]-(j==k)>0),F()) for k in range(4)] for j in range(4)] for p in row] for row in P]
def point_and_gradient(poly,z):
    powers=[[x**n for n in range(9)] for x in z]
    value=F();gradient=[F()]*4
    for e,c in poly.items():
        value+=c*prod(powers[j][e[j]] for j in range(4))
        for k in range(4):
            if e[k]:
                gradient[k]+=c*e[k]*prod(powers[j][e[j]-(j==k)] for j in range(4))
    return value,gradient
def decode(path):
    assert len(path)%2==0
    bounds=[[-F(1),F(1)] for _ in range(4)]
    for j in range(0,len(path),2):
        axis,bit=int(path[j]),int(path[j+1]);assert axis in range(4) and bit in (0,1)
        middle=sum(bounds[axis])/2
        bounds[axis][1-bit]=middle
    return tuple(tuple(pair) for pair in bounds)
def fields(box,site):
    z=tuple((a+b)/2 for a,b in box);h=tuple((b-a)/2 for a,b in box)
    points=tuple(c+hh*x for c,hh,x in zip(C[site],H,z))
    whole=tuple((c+hh*a,c+hh*b) for c,hh,(a,b) in zip(C[site],H,box))
    values=[]
    for k in range(4):
        cp,cg=point_and_gradient(P[site][k],z)
        group=2*(k//2)
        charts=[0] if whole[group][0]>=whole[group+1][1] else [1] if whole[group+1][0]>=whole[group][1] else [0,1]
        ranges=[]
        for chart in charts:
            axis=group+chart;m=points[axis];factor=F(3,2)-1/(2*m*m)
            value=points[k]*factor+cp
            grad=list(cg);grad[k]+=H[k]*factor;grad[axis]+=H[axis]*points[k]/m**3
            hm=[[F() for _ in range(4)] for _ in range(4)]
            mlo=C[site][axis]-H[axis];xhi=C[site][k]+H[k];assert mlo>0
            if k==axis:hm[axis][axis]=1/mlo**3
            else:
                hm[axis][axis]=3*xhi/mlo**4
                hm[k][axis]=hm[axis][k]=1/mlo**3
            radius=sum((abs(g)*hh for g,hh in zip(grad,h)),F())
            radius+=sum(((HESS[site][k][j][l]+hm[j][l]*H[j]*H[l])*h[j]*h[l]/2 for j in range(4) for l in range(4)),F())
            ranges.append((value-radius,value+radius))
        values.append((min(a for a,b in ranges),max(b for a,b in ranges)))
    return values
def density_lower(box):
    a,b=fields(box,0),fields(box,1)
    if a[0][1]>max(F(),a[2][0]):return F()
    return max(F(),min(40*(max(F(),a[3][0])-a[1][1]),
        F(20,3)*(max(F(),b[2][0])-b[0][1]),
        40*(b[1][0]-max(F(),b[3][1]))))
def old_disjoint():
    # Whole endpoint roots have ownmax<=.8, opponentmax>=.82 and ownmin>=.425.
    lower=F(17,40);upper=F(4,5);opp=F(41,50)
    old=json.loads((AUCTION/'V4_8A_frozen_primal/certificate/master_certificate.json').read_text())
    for cell in old['cells']:
        assert max(F(c)-F(h) for c,h in zip(cell['center'][:2],cell['halfwidths'][:2]))>upper
        assert max(F(c)-F(h) for c,h in zip(cell['center'][2:],cell['halfwidths'][2:]))>upper
    old=json.loads((AUCTION/'V4_7/certificate/psd_local_certificate.json').read_text())
    for witness in old['witnesses']:
        for cell in witness['selected_symmetry_orbits']:
            lo=[F(c)-F(h) for c,h in zip(cell['center'],cell['halfwidths'])]
            hi=[F(c)+F(h) for c,h in zip(cell['center'],cell['halfwidths'])]
            assert (max(hi)<opp or (max(lo[:2])>upper and max(lo[2:])>upper))
    old=json.loads((AUCTION/'V4_6_2_upper/certificate/sparse_cycle.json').read_text())
    for center in old['orbit_centers']:
        lo=[F(c)-F(h) for c,h in zip(center,old['halfwidths'])]
        hi=[F(c)+F(h) for c,h in zip(center,old['halfwidths'])]
        assert max(hi)<opp or any(max(hi[2*b:2*b+2])<opp and min(hi[2*b:2*b+2])<lower for b in (0,1))
def calculate():
    data=json.loads((ROOT/'certificate/bb_global_input.json').read_text())
    assert data['scale']==1<<20
    boxes=[];gain=F();mass=F();checks=[];ic_upper=F();capacity_release=F();strict_full_pairs=0
    for n,cell in enumerate(data['cells']):
        box=decode(cell['path']);lam=F(cell['density_numerator'],data['scale']);assert lam>0
        lower=density_lower(box);assert lam<=lower,(n,float(lam),float(lower))
        for other in boxes:assert any(b<=c or d<=a for (a,b),(c,d) in zip(box,other))
        boxes.append(box)
        volume=VOLUME*prod((b-a)/2 for a,b in box)
        gain+=4*F(1,40)*lam*volume;mass+=8*lam*volume
        picks=[]
        for site in range(2):
            physical=[menus.I(c+h*a,c+h*b) for c,h,(a,b) in zip(C[site],H,box)]
            assert physical[0].lo+physical[1].lo>menus.b
            assert physical[2].lo>menus.T
            picks.append(menus.construct('base',physical[:2],physical[2:],0))
        assert picks[0]['allocation']==((F(),F()),(F(1),F(1)))
        assert set(picks[1]['possible'])<=set(['empty','item2','bundle'])
        uncertain=picks[1]['ae_winner']!='item2'
        ic_upper+=4*lam*volume*F(3,20)*uncertain
        capacity_release+=4*lam*volume*F(1,40)*uncertain
        strict_full_pairs+=int(not uncertain)
        checks.append(dict(path=cell['path'],certified_density_lower=str(lower),chosen_density=str(lam),volume=str(volume)))
    old_disjoint()
    assert 0<gain<F(1,1000000)
    return dict(status='BB_NONCOMPLEMENTARY_GLOBAL_FLOW_GAIN_PASS',
        exact_upper_decrease=str(gain),display_upper_decrease=float(gain),
        positive_leaf_pairs=len(boxes),symmetry_copies=4,finite_IC_measure_mass=str(mass),
        exact_added_IC_interval_at_incumbent=['0',str(ic_upper)],
        regional_ledger=dict(region='BB',capacity_slack_change_interval=[str(-capacity_release),'0'],weighted_IC_change_interval=['0',str(ic_upper)],
            virtual_slack_change_interval=[str(-gain-ic_upper),str(-gain)],
            screening_source_boundary_changes='0',net_gap_change=str(-gain),constant_safe_pairs=strict_full_pairs,
            correlated_pointwise_identity='Writing g=lambda/40, h=3lambda/20, ownB=(a1,a2), opponentB=(b1,b2): deltaC=-g(1-a2-b2), deltaK=h*a1+g(1-a2), deltaV=-g-h*a1-g*b2; sum=-g.'),
        source_sink='Balanced two-way IC pairs cancel every utility marginal exactly.',
        boundary_singular_terms='No integration by parts is invoked; the pair measure has absolutely continuous report allocation covectors and no singular capacity term.',
        complete_accounting='R=<Phi_new,x>-K_old-K_new-IR_old-screening_old; all old supports are disjoint.',
        new_gap_identity='G_new=G_old-exact_upper_decrease, with added K_new retained; intermediate complementarity is not required.',
        checks=checks,independence='Exact Fraction monomial values, gradients, Hessian bounds and chart unions; no discovery arithmetic imported.',
        imported_independent_coefficient_source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
        incumbent_menu_classifier_sha256=sha256(MENU_SOURCE.read_bytes()).hexdigest(),
        input_sha256=sha256((ROOT/'certificate/bb_global_input.json').read_bytes()).hexdigest())
if __name__=='__main__':
    out=calculate();p=ROOT/'certificate/bb_global.json'
    if '--write' in sys.argv:p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    else:assert json.loads(p.read_text(encoding='utf-8'))==out
    print(out['status'],out['exact_upper_decrease'],out['display_upper_decrease'])
