"""Independent rational algebra for V4.6 inner certificates.

No V4.6 verifier or predecessor module is imported. These checks supplement
the analytic all-competitor argument; they do not prove it by examples.
Run with python -X utf8 -B, without -O. Default execution compares stored JSON
without writing; --write regenerates only this audit folder's JSON result.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import hashlib
import json
import sys

if not __debug__ or sys.flags.optimize:
    raise RuntimeError("Assertions must be enabled")


def add(*ps):
    out = {}
    for p in ps:
        for d, a in p.items():
            out[d] = out.get(d, Q()) + a
    return {d: a for d, a in out.items() if a}


def scale(p, a):
    return {d: a*b for d, b in p.items() if a*b}


def mul(p, r):
    out = {}
    for d, a in p.items():
        for e, b in r.items():
            out[d+e] = out.get(d+e, Q()) + a*b
    return {d: a for d, a in out.items() if a}


def power(p, n):
    out = {0: Q(1)}
    for _ in range(n):
        out = mul(out, p)
    return out


def val(p, x):
    return sum((a*x**d for d, a in p.items()), Q())


def integral(p, lo, hi):
    return sum((a*(hi**(d+1)-lo**(d+1))/(d+1) for d, a in p.items()), Q())


def constant(a):
    return {0: Q(a)} if a else {}


def trace(p, axis, fixed):
    out = {}
    for (i, j), a in p.items():
        d, b = (j, a*fixed**i) if axis == 0 else (i, a*fixed**j)
        out[d] = out.get(d, Q()) + b
    return out


def derivative(p, axis):
    out = {}
    for ij, a in p.items():
        ds = list(ij)
        if ds[axis]:
            b = a*ds[axis]
            ds[axis] -= 1
            out[tuple(ds)] = b
    return out


def times_linear(p, axis, intercept, slope, other_slope=Q()):
    out = {}
    for ij, a in p.items():
        out[ij] = out.get(ij, Q()) + a*intercept
        for coordinate, factor in ((axis, slope), (1-axis, other_slope)):
            ds = list(ij)
            ds[coordinate] += 1
            out[tuple(ds)] = out.get(tuple(ds), Q()) + a*factor
    return out


def region(p, axis, lo, hi, intercept, slope):
    """Integrate p where inner coordinate ranges [intercept+slope*outer,1]."""
    out = Q()
    for ij, a in p.items():
        inner, outer = ij[axis], ij[1-axis]
        n = inner+1
        out += a*(hi**(outer+1)-lo**(outer+1))/(n*(outer+1))
        for j in range(n+1):
            coef = a*comb(n,j)*intercept**(n-j)*slope**j/n
            out -= coef*(hi**(outer+j+1)-lo**(outer+j+1))/(outer+j+1)
    return out


def square(p):
    return sum((a/((i+1)*(j+1)) for (i,j),a in p.items()), Q())


def revenue(u):
    return sum(((i+j-1)*a/((i+1)*(j+1)) for (i,j),a in u.items()), Q())


def tail_price(fpieces, allocation, anchor=None, mass=Q()):
    accumulated = Q()
    out = Q()
    for lo, hi, f in fpieces:
        primitive = {d+1: a/(d+1) for d,a in f.items()}
        negative_prefix = add(constant(-accumulated+val(primitive,lo)),scale(primitive,-1))
        if anchor is None:
            pieces = [(lo,hi,negative_prefix)]
        else:
            pieces = []
            if lo < min(anchor,hi):
                pieces.append((lo,min(anchor,hi),negative_prefix))
            if max(lo,anchor) < hi:
                pieces.append((max(lo,anchor),hi,add(negative_prefix,constant(mass))))
        for left,right,weight in pieces:
            out += integral(mul(weight,allocation),left,right)
        accumulated += integral(f,lo,hi)
    assert accumulated == mass
    return out


A, q, c = Q(2,3), Q(113,500), Q(137,500)
T, U = Q(613,750), Q(839,750)
X = {1: Q(1)}
AL = add(scale(X,3),constant(-2))
DELTA = add(constant(q+3*q*q/4),scale(X,-3*q/2),scale(power(AL,2),Q(1,16)))
assert DELTA == scale(mul(add(constant(T),scale(X,-1)),add(constant(U),scale(X,-1))),Q(9,16))
K = add(X,constant(-q))
J = add(constant(1),scale(X,-Q(1,2)))
B = add(constant(Q(1,2)),DELTA)
C = add(X,constant(c),DELTA)
L = add(DELTA,scale(AL,Q(1,2)))
Y = add(constant(c),L)
mass_lottery = add(mul(add(scale(B,3),constant(-2)),K),
                   mul(add(scale(C,3),constant(-2)),add(J,scale(K,-1))),
                   scale(add(power(J,2),scale(power(K,2),-1)),-Q(3,2)),
                   mul(add(scale(Y,3),constant(-2)),add(constant(A),scale(J,-1))),
                   constant(1-A))
assert not mass_lottery
assert add(C,scale(Y,-1),scale(J,-1)) == {}
assert val(L,T) == q
assert 3*(A-q)*q-2*q*(c+q/4) == q*(1-3*q/2) > 0

# Exact polynomial identity in C and k, by monomial coefficients.
# 3[k(C-k)+C(A-k)-(A^2-k^2)/2] - [2C-5/3-3k^2/2] = 1.
area_identity = {(1,0): 3*A-2, (0,2): -3+Q(3,2)+Q(3,2),
                 (0,0): -3*A*A/2+Q(5,3)-1}
assert all(v == 0 for v in area_identity.values())


def lottery_check(t,u):
    delta = val(DELTA,t)
    alpha = 3*t-2
    beta = alpha/(alpha+2*delta)
    k,j = t-q,1-t/2
    b,cc,length = Q(1,2)+delta,t+c+delta,delta+alpha/2
    yy,lam = c+length,alpha*(c+length/4)
    ax,ay = derivative(u,0),derivative(u,1)
    g,atop,aline = trace(u,0,1),trace(ax,1,1),trace(ax,1,c)
    G = [(Q(),c,t,Q()),(c,yy,t+beta*c,-beta),(yy,Q(1),A,Q())]
    H = [(Q(),k,b,Q()),(k,j,cc,Q(-1)),(j,A,yy,Q())]
    d0 = square(u)
    volume = Q()
    for axis,pieces,allocation in ((0,G,ax),(1,H,ay)):
        for lo,hi,intercept,slope in pieces:
            d0 -= region(u,axis,lo,hi,intercept,slope)
            density_times_a = times_linear(allocation,axis,-3*intercept,Q(3),-3*slope)
            volume += region(density_times_a,axis,lo,hi,intercept,slope)
    f = [(Q(),k,constant(3*b-2)),(k,j,{0:3*cc-2,1:Q(-3)}),
         (j,A,constant(3*yy-2)),(A,Q(1),constant(1))]
    top = tail_price(f,atop)
    line = 3*t*(c+length/4)*integral(aline,A,t)+lam*integral(aline,t,1)
    sigma = alpha*integral(g,0,c)+integral(mul({0:alpha+3*beta*c,1:-3*beta},g),c,yy)
    tg = lam*val(g,c)-sigma
    ma = t/(t-A)*integral(aline,A,t)-integral(aline,0,t)
    su = 3*d0-lam*val(trace(u,0,0),c)
    # The trace is quadratic here. This separately evaluates the hinge measure term.
    gsecond = 2*g.get(2,Q())
    hinge = alpha*(c*val(g,c)-integral(g,0,c)) + beta*gsecond*length**4/24
    assert tg == hinge
    gap = volume+top+line-revenue(u)
    assert gap == tg+lam*ma+su
    assert min(tg,ma,su) >= 0
    return dict(t=str(t),revenue=str(revenue(u)),gap=str(gap),
                trace_slack=str(tg),monotonicity_slack=str(ma),sink_slack=str(su))


def diagonal_check(b,cc,u):
    k = cc-b
    mass = 2*cc-Q(5,3)-3*k*k/2
    assert 0 < k < Q(1,2) < A and b <= A and mass > 0
    ax,ay = derivative(u,0),derivative(u,1)
    G = [(Q(),Q(1),A,Q())]
    H = [(Q(),k,b,Q()),(k,A,cc,Q(-1))]
    d0,volume = square(u),Q()
    for axis,pieces,allocation in ((0,G,ax),(1,H,ay)):
        for lo,hi,intercept,slope in pieces:
            d0 -= region(u,axis,lo,hi,intercept,slope)
            volume += region(times_linear(allocation,axis,-3*intercept,Q(3),-3*slope),axis,lo,hi,intercept,slope)
    f = [(Q(),k,constant(3*b-2)),(k,A,{0:3*cc-2,1:Q(-3)}),(A,Q(1),constant(1))]
    top = tail_price(f,trace(ax,1,1),Q(1,2),mass)
    bottom = mass*integral(trace(ax,1,0),0,Q(1,2))
    vertical = mass*integral(trace(ay,0,Q(1,2)),0,1)
    sink = 3*d0-mass*u.get((0,0),Q())
    gap = volume+top+bottom+vertical-revenue(u)
    assert gap == sink >= u.get((0,0),Q()) >= 0
    return dict(B=str(b),C=str(cc),mass=str(mass),revenue=str(revenue(u)),gap=str(gap),sink=str(sink))


families = {
    "smooth_full_range_randomized": {(2,0):Q(1,4),(1,1):Q(1,2),(0,2):Q(1,4)},
    "smooth_interior_randomized_with_positive_origin_rent": {
        (0,0):Q(1),(1,0):Q(1,5),(0,1):Q(1,10),
        (2,0):Q(3,20),(1,1):Q(1,10),(0,2):Q(1,5)},
}
rows = []
for name,u in families.items():
    for t in (Q(67,100),Q(7,10),Q(3,4),Q(4,5)):
        rows.append(dict(family=name,kind="lottery",**lottery_check(t,u)))
    rows.append(dict(family=name,kind="diagonal_symmetric",**diagonal_check(A,Q(9,10),u)))
    rows.append(dict(family=name,kind="diagonal_constrained",**diagonal_check(Q(91,100)-(Q(27,50)-q),Q(91,100),u)))

# Explicit harmless counterexample to the literal statement u*=0 on all D0.
t = Q(7,10)
delta = val(DELTA,t)
yy = c+delta+(3*t-2)/2
cc = t+c+delta
assert yy < 1 and A+1-cc > 0
boundary_note = dict(t=str(t),point=[str(A),"1"],candidate_utility=str(A+1-cc),
                     reason="x=A lies in neither G nor H; positive utility on a two-dimensional null boundary")

source = Path(__file__).resolve().parents[2]/"V4_6"
hashes = {}
for rel in ("research_log/inner_lottery_certificate.md","research_log/inner_diagonal_capacity.md",
            "research_log/conditional_coverage.md","verifier/price_joint_reallocation.py"):
    hashes[rel] = hashlib.sha256((source/rel).read_bytes()).hexdigest()
data = dict(status="FRESH_INDEPENDENT_DUAL_ALGEBRA_PASS",source_hashes=hashes,
            symbolic_identities=["lottery delta factorization", "lottery zero top mass", "C-Y=j",
                                 "lottery uniform sink margin", "diagonal area equals (m+1)/3"],
            exact_smooth_competitor_checks=rows,nonblocking_boundary_wording=boundary_note,
            scope="Exact algebra and smooth arbitrary-range randomized regressions; analytic proof audit is separate")
destination = Path(__file__).with_name("fresh_exact_dual_checks.json")
if '--write' in sys.argv:
    destination.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
else:
    assert json.loads(destination.read_text(encoding="utf-8")) == data
print(data["status"])
print("smooth_competitor_cases",len(rows))
print("nonblocking_boundary_wording",json.dumps(boundary_note))
