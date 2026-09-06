"""Self-contained BASE-1 mechanism, reconstructed from the named sealed tables.

Only the sibling V3 certificate JSON is read. All computations are rational.
Masks 0,1,2,3 denote empty, item 1, item 2, and the bundle. The shared base
outcome is essential to the pointwise tie convention; prices alone do not
authorize independent tie-breaking by the two bidders.
"""
from fractions import Fraction as F
import json
from pathlib import Path

DATA = json.loads((Path(__file__).parents[1] / "certificate" /
                   "baseline_mechanism.json").read_text(encoding="utf-8"))
A = F(DATA["parameters"]["a"])
B = F(DATA["parameters"]["b"])
S = F(DATA["parameters"]["split_cost"])
C, D = B - A, S - A
OUTCOMES = [tuple(row) for row in DATA["base_outcome_order"]]
COSTS = [F(0), A, A, B, A, A, B, S, S]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def value(type_, mask):
    return sum((type_[j] for j in range(2) if mask & (1 << j)), F())


def pivot(q):
    return max(F(), q[0] - A, q[1] - A, q[0] + q[1] - B)


def base_menu(q):
    H = pivot(q)
    prices = (F(), H + min(A, S - q[1]), H + min(A, S - q[0]), H + B)
    require(prices[1] + prices[2] - prices[3] >= S - B,
            "global strict base-menu subadditivity")
    return prices


def fee_rows(q):
    """Literal first-match rule, including every boundary report."""
    high, low = max(q), min(q)
    for row in DATA["common_rows"]:
        left, right = map(F, row["high_interval"])
        cap = B - high if row["id"].startswith("Z") else C
        if left <= high <= right and 0 <= low <= cap:
            return F(row["fee"]), row["id"]
    total = high + low
    if B <= total <= 1 and C <= low <= total - D:
        denominator = total - C - D
        require(denominator >= F(27, 200), "bundle coordinate denominator")
        ratio = (low - C) / denominator
        for row in DATA["bundle_rows"]:
            left, right = map(F, row["sum_interval"])
            down, up = map(F, row["normalized_rho_interval"])
            if left <= total <= right and down <= ratio <= up:
                return F(row["fee"]), row["id"]
    return F(), None


def menu(q):
    """Return prices and row metadata; this function depends only on q."""
    q = tuple(map(F, q))
    require(len(q) == 2 and all(0 <= x <= 1 for x in q), "opponent domain")
    prices0 = base_menu(q)
    fee, common_id = fee_rows(q)
    before = tuple(p + fee if mask else F() for mask, p in enumerate(prices0))
    prices = list(before)
    item_id, delta, low_mask = None, F(), None
    if common_id in ("S5.1", "S5.2"):
        high = max(q)
        for row in DATA["item_rows"]:
            left, right = map(F, row["high_interval"])
            if row["parent"] == common_id and left < high <= right:
                require(q[0] != q[1], "item row must have a unique low coordinate")
                low_mask = 1 if q[0] < q[1] else 2
                item_id, delta = row["id"], F(row["item_surcharge"])
                require(F(row["common_fee"]) == fee, "item/common fee identity")
                prices[low_mask] += delta
                prices[3] += delta
                break
    return {"prices": tuple(prices), "base_prices": prices0,
            "common_prices": before, "common_fee": fee,
            "common_row": common_id, "item_row": item_id,
            "item_delta": delta, "changed_singleton": low_mask}


def mechanism(profile):
    """Evaluate exact allocation, normalized payments, utilities, and row ids."""
    profile = tuple(map(F, profile))
    require(len(profile) == 4 and all(0 <= x <= 1 for x in profile), "type domain")
    types = (profile[:2], profile[2:])
    scores = [value(types[0], masks[0]) + value(types[1], masks[1]) - cost
              for masks, cost in zip(OUTCOMES, COSTS)]
    best = max(scores)
    base_id = next(i for i, score in enumerate(scores) if score == best)
    base_masks = OUTCOMES[base_id]
    final_masks, payments, utilities, metadata = [], [], [], []
    for bidder in range(2):
        own, opponent = types[bidder], types[1 - bidder]
        info = menu(opponent)
        predecessor = base_masks[bidder]
        base_utility = value(own, predecessor) - info["base_prices"][predecessor]
        require(base_utility == best - pivot(opponent), "base/menu payment identity")
        common_utilities = [value(own, mask) - price
                            for mask, price in enumerate(info["common_prices"])]
        common_maximum = max(common_utilities)
        if common_maximum == 0:
            predecessor = 0
        else:
            require(common_utilities[predecessor] == common_maximum,
                    "common fee must retain the shared base bundle")
        all_utilities = [value(own, mask) - price
                         for mask, price in enumerate(info["prices"])]
        maximum = max(all_utilities)
        if maximum == 0:
            selected = 0
        elif all_utilities[predecessor] == maximum:
            selected = predecessor
        else:
            subsets = [mask for mask in range(4)
                       if mask & ~predecessor == 0 and all_utilities[mask] == maximum]
            require(bool(subsets), "deletion-containment maximizer missing")
            selected = min(subsets)
        require(selected & ~predecessor == 0, "item-stage deletion")
        require(selected & ~base_masks[bidder] == 0, "base-stage deletion")
        require(all_utilities[selected] == maximum >= 0, "DSIC menu maximization/IR")
        final_masks.append(selected)
        payments.append(info["prices"][selected])
        utilities.append(maximum)
        info["common_predecessor_mask"] = predecessor
        metadata.append(info)
    require(final_masks[0] & final_masks[1] == 0, "joint item capacity")
    return {"profile": profile, "base_id": base_id, "base_masks": base_masks,
            "masks": tuple(final_masks), "payments": tuple(payments),
            "utilities": tuple(utilities), "menus": tuple(metadata)}


def allocation_vector(result):
    return tuple(F(bool(mask & (1 << item)))
                 for mask in result["masks"] for item in range(2))


if __name__ == "__main__":
    for p in ((F(321, 500), 0, F(539, 1000), 0),
              (F(643, 1000), 0, F(541, 1000), 0)):
        result = mechanism(p)
        print("profile", result["profile"], "allocation", result["masks"],
              "payments", result["payments"])
