"""Exact adaptive Bernstein refinement for the frozen rational degree-4 stream."""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import time
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
import degree4_polynomials as higher
import dual_polynomials as dp
import fixed_bernstein as verify

TARGET = Q(372431922023109, 419430400000000)
INCUMBENT = Q(1865971568546293, 2097152000000000)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    digest = hashlib.sha256()
    digest.update(Path(path).read_bytes())
    return digest.hexdigest()


def load_frozen():
    local = HERE / "candidate_degree4_exact.json"
    data = json.loads(local.read_text(encoding="utf-8"))
    basis = higher.basis_exponents()
    require(data["basis_order"] == [list(pair[0]) for pair in basis],
            "candidate basis order mismatch")
    theta = [Q(x) for x in data["theta"]]
    require(len(theta) == len(basis) == 32, "candidate dimension mismatch")
    return theta, basis, local


def primitive(first, fe, second, se, difference, de):
    fmin, fmax = int(first.min()), int(first.max())
    smin, smax = int(second.min()), int(second.max())
    dmin, dmax = int(difference.min()), int(difference.max())
    if fmin - fe >= 0 and dmin - de >= 0:
        return True, verify.mean_upper_integer(first, fe), "first"
    if smin - se >= 0 and dmax + de <= 0:
        return True, verify.mean_upper_integer(second, se), "second"
    if fmax + fe <= 0 and smax + se <= 0:
        return True, 0, "zero"
    return False, max(0, fmax + fe, smax + se), "unresolved"


def split_all(first, fe, second, se, difference, de, axis):
    fl, fr, fd = verify.split_floor(first, axis)
    sl, sr, sd = verify.split_floor(second, axis)
    dl, dr, dd = verify.split_floor(difference, axis)
    errors = (fe + fd, se + sd, de + dd)
    return (fl, sl, dl, errors), (fr, sr, dr, errors)


def best_local(first, fe, second, se, difference, de, extra):
    fixed, bound, winner = primitive(first, fe, second, se, difference, de)
    if fixed or extra == 0:
        return bound << extra, {"kind": winner, "bound": bound, "children": []}
    baseline = bound << extra
    best_value = baseline
    best_plan = {"kind": "hold", "bound": bound, "children": []}
    for axis in range(4):
        children = split_all(first, fe, second, se, difference, de, axis)
        child_results = [best_local(a, e[0], b, e[1], d, e[2], extra - 1)
                         for a, b, d, e in children]
        value = sum(item[0] for item in child_results)
        if value < best_value:
            best_value = value
            best_plan = {"kind": "split", "axis": axis, "bound": bound,
                         "children": [item[1] for item in child_results]}
    return best_value, best_plan


def count_plan(plan, stats):
    if plan["kind"] == "split":
        stats["adaptive_splits"] += 1
        stats["adaptive_axis_counts"][plan["axis"]] += 1
        for child in plan["children"]:
            count_plan(child, stats)
    else:
        stats["adaptive_terminal_kinds"][plan["kind"]] = (
            stats["adaptive_terminal_kinds"].get(plan["kind"], 0) + 1
        )


def decode_path(path):
    lo = [Q(0)] * 4
    hi = [Q(1)] * 4
    for axis, side in path:
        mid = (lo[axis] + hi[axis]) / 2
        if side == 0:
            hi[axis] = mid
        else:
            lo[axis] = mid
    return [str(x) for x in lo], [str(x) for x in hi]


def run(base_depth, extra, scale, *, write_outputs=True, emit=True,
        include_runtime=True):
    started = time.perf_counter()
    theta, basis, candidate_path = load_frozen()
    final_depth = base_depth + extra
    stats = {
        "base_fixed": 0, "base_unresolved": 0, "base_refined": 0,
        "base_held": 0, "adaptive_splits": 0,
        "adaptive_axis_counts": [0, 0, 0, 0],
        "adaptive_terminal_kinds": {}, "gain_units": 0,
    }
    chart_stats = {f"{a}{b}": {"unresolved": 0, "refined": 0, "gain_units": 0}
                   for a in range(2) for b in range(2)}
    gain_hist = {"zero": 0, "lt_1e5": 0, "lt_1e6": 0,
                 "lt_1e7": 0, "lt_1e8": 0, "ge_1e8": 0}
    top = []
    serial = 0
    accumulator = 0
    max_control = 0

    def hist_key(gain):
        if gain == 0: return "zero"
        if gain < 10**5: return "lt_1e5"
        if gain < 10**6: return "lt_1e6"
        if gain < 10**7: return "lt_1e7"
        if gain < 10**8: return "lt_1e8"
        return "ge_1e8"

    for c1 in range(2):
        for c2 in range(2):
            first_poly, second_poly = higher.competitors(theta, basis, c1, c2)
            difference_poly = dp.add(first_poly, dp.scale(second_poly, -1))
            first = verify.fixed_controls(first_poly, scale)
            second = verify.fixed_controls(second_poly, scale)
            difference = verify.fixed_controls(difference_poly, scale)
            max_control = max(max_control, *(abs(int(x)) for a in (first, second, difference)
                                             for x in (a.min(), a.max())))

            def recurse(a, ae, b, be, d, de, remaining, level, path):
                nonlocal serial
                fixed, bound, _ = primitive(a, ae, b, be, d, de)
                if fixed:
                    stats["base_fixed"] += 1
                    return bound << (final_depth - level)
                if remaining == 0:
                    stats["base_unresolved"] += 1
                    chart = chart_stats[f"{c1}{c2}"]
                    chart["unresolved"] += 1
                    baseline = bound << extra
                    value, plan = best_local(a, ae, b, be, d, de, extra)
                    gain = baseline - value
                    stats["gain_units"] += gain
                    chart["gain_units"] += gain
                    gain_hist[hist_key(gain)] += 1
                    if gain:
                        stats["base_refined"] += 1
                        chart["refined"] += 1
                        count_plan(plan, stats)
                    else:
                        stats["base_held"] += 1
                    serial += 1
                    if gain and (len(top) < 50 or gain > top[0][0]):
                        lo, hi = decode_path(path)
                        record = {"gain_units": gain, "chart": [c1, c2],
                                  "base_bound_units": bound, "lo": lo, "hi": hi,
                                  "root_plan_kind": plan["kind"],
                                  "root_axis": plan.get("axis")}
                        heapq.heappush(top, (gain, serial, record))
                        if len(top) > 50:
                            heapq.heappop(top)
                    return value
                if remaining <= 4:
                    candidates = []
                    for axis in range(4):
                        children = split_all(a, ae, b, be, d, de, axis)
                        score = sum(primitive(x, e[0], y, e[1], z, e[2])[1]
                                    for x, y, z, e in children)
                        candidates.append((score, axis, children))
                    _, axis, children = min(candidates, key=lambda x: (x[0], x[1]))
                else:
                    axis = verify.choose_axis(a, b, d)
                    children = split_all(a, ae, b, be, d, de, axis)
                return sum(recurse(x, e[0], y, e[1], z, e[2], remaining - 1,
                                   level + 1, path + ((axis, side),))
                           for side, (x, y, z, e) in enumerate(children))

            accumulator += recurse(first, 1, second, 1, difference, 1,
                                   base_depth, 0, ())

    upper = Q(2 * accumulator, scale * (1 << final_depth))
    improvement = Q(2 * stats["gain_units"], scale * (1 << final_depth))
    runtime = time.perf_counter() - started
    report = {
        "status": "EXACT_ADAPTIVE_FIXED_POINT_UPPER",
        "candidate": candidate_path.name, "base_depth": base_depth,
        "adaptive_extra_depth": extra, "common_final_depth": final_depth,
        "scale": scale, "maximum_initial_absolute_control": max_control,
        "accumulator": str(accumulator), "upper_fraction": str(upper),
        "upper_float": float(upper), "target_fraction": str(TARGET),
        "target_float": float(TARGET), "strictly_below_target": upper < TARGET,
        "strictly_below_incumbent": upper < INCUMBENT,
        "adaptive_improvement_fraction": str(improvement),
        "adaptive_improvement_float": float(improvement),
        "statistics": stats, "chart_decomposition": chart_stats,
        "gain_histogram": gain_hist,
        "top_gain_boxes": [x[2] for x in sorted(top, reverse=True)],
    }
    if include_runtime:
        report["runtime_seconds"] = runtime
    text = json.dumps(report, indent=2)
    if write_outputs:
        stem = f"adaptive_degree4_base{base_depth}_extra{extra}_s{scale}"
        result_path = HERE / f"{stem}.json"
        result_path.write_text(text, encoding="utf-8")
        (HERE / f"{stem}.log").write_text(text + "\n", encoding="utf-8")
        hashes = {path.name: sha256(path)
                  for path in (Path(__file__), candidate_path, result_path)}
        (HERE / f"hashes_extra{extra}_s{scale}.json").write_text(
            json.dumps(hashes, indent=2), encoding="utf-8")
    if emit:
        print(text)
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-depth", type=int, default=20)
    ap.add_argument("--extra", type=int, choices=(1, 2), required=True)
    ap.add_argument("--scale", type=int, default=10**9)
    a = ap.parse_args()
    run(a.base_depth, a.extra, a.scale)
