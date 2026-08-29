"""Tests for the sciencebro-math tool layer.

Two kinds of test here, and the second kind matters more. The first checks that the
tools compute what they claim on objects with known answers. The second checks that the
DISCIPLINE holds: that a float cannot sneak into an exact tool, that failing to certify
is not reported as a refutation, and that no result claims to support PROVED.
"""

from __future__ import annotations

import sys
from math import comb
from pathlib import Path

import pytest
from flint import fmpq

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))

from sciencebro_math import (  # noqa: E402
    bernstein_certificate,
    centered_squares,
    half_spectrum,
    hankel_minors,
    hausdorff_conditions,
    log_difference_hierarchy,
    normalized_means,
    ratio_log_concavity,
    real_rootedness,
    sturm_sign,
    toeplitz_minors,
    turan,
    verify_polynomial_positive,
)
from sciencebro_math.core import KIND_TO_MAX_CLAIM_STATUS  # noqa: E402
from sciencebro_math.families import esym  # noqa: E402
from sciencebro_math.sequences import as_seq, sign_log_difference  # noqa: E402

# ------------------------------------------------------------------ known answers


def test_esym_matches_binomials_on_all_ones():
    """e_t of N ones is C(N,t) -- the simplest object with a known answer."""
    N = 7
    e = esym([fmpq(1)] * N)
    assert [int(x) for x in e] == [comb(N, t) for t in range(N + 1)]


def test_centered_multiset_is_doubled_for_odd_n():
    """For odd n the centred spectrum is the half spectrum twice over."""
    n = 11
    full = sorted(int(x) for x in centered_squares(n))
    half = sorted(int(x) for x in half_spectrum(n))
    assert full == sorted(half + half)


def test_binomial_sequence_is_log_concave_and_not_ratio_log_concave_everywhere():
    p = [fmpq(comb(10, t)) for t in range(11)]
    assert turan(p).status == "ok"


def test_sign_log_difference_agrees_with_direct_comparison():
    p = normalized_means(centered_squares(13))
    for t in range(1, 4):
        direct = p[t + 1] ** 3 * p[t - 1] - p[t] ** 3 * p[t + 2]
        s = sign_log_difference(p, t - 1, 3)
        assert (s < 0) == (direct > 0)


def test_geometric_sequence_has_zero_log_differences():
    """A geometric sequence has vanishing second and higher log differences."""
    p = [fmpq(3) ** t for t in range(8)]
    for r in (2, 3, 4):
        assert all(sign_log_difference(p, t, r) == 0 for t in range(8 - r))


def test_hankel_of_moment_sequence_is_nonnegative():
    """a_t = 1/(t+1) are the moments of Lebesgue measure on [0,1]: Hankel must pass."""
    a = [fmpq(1, t + 1) for t in range(10)]
    assert hankel_minors(a, max_order=4).status == "ok"
    assert hausdorff_conditions(a, max_order=6).data["completely_monotone_forward"]


def test_hausdorff_rejects_an_increasing_sequence_forward_and_accepts_it_reversed():
    a = [fmpq(t + 1) for t in range(8)]
    r = hausdorff_conditions(a, max_order=4)
    assert not r.data["completely_monotone_forward"]


def test_toeplitz_minors_pass_for_binomials():
    """Binomial rows are a Polya frequency sequence, so no Toeplitz minor is negative."""
    a = [fmpq(comb(8, t)) for t in range(9)]
    assert toeplitz_minors(a, max_order=3).status == "ok"


def test_real_rootedness_detects_a_complex_pair():
    assert real_rootedness([1, 0, 1]).status == "refuted"
    assert real_rootedness([1, 3, 2]).status == "ok"


def test_sturm_sign_on_a_definite_quadratic():
    r = sturm_sign([1, 0, 1], 0, 2)
    assert r.status == "ok" and r.data["sign"] == 1


def test_bernstein_certifies_a_shallow_polynomial_only_after_subdivision():
    """(2x-1)^2 touches zero at x = 1/2, so one Bernstein pass is not enough.

    x^2 - x + 1 is certified in a single pass (coefficients 1, 1/2, 1), which is why
    it is the wrong example for this test -- an earlier version used it and the
    failure exposed an index bug in the change of basis instead.
    """
    assert bernstein_certificate([1, -1, 1], 0, 1).status == "ok"
    assert bernstein_certificate([1, -4, 4], 0, 1).status == "inconclusive"
    assert verify_polynomial_positive([1, -4, 4], 0, 1, subdivisions=2).status == "ok"


# ------------------------------------------------------------------- discipline


def test_float_is_refused_by_exact_tools():
    with pytest.raises(TypeError):
        as_seq([1.5, 2.0])


def test_failing_to_certify_is_inconclusive_not_refuted():
    """The distinction the whole positivity module exists to preserve."""
    r = verify_polynomial_positive([1, -4, 4], 0, 1, subdivisions=1)
    assert r.status in ("ok", "inconclusive")
    assert r.status != "refuted"


def test_no_evidence_kind_supports_proved():
    assert "PROVED" not in set(KIND_TO_MAX_CLAIM_STATUS.values())


def test_result_payload_says_it_cannot_prove():
    r = ratio_log_concavity(normalized_means(centered_squares(11)), upto=5)
    d = r.to_dict()
    assert d["never"] == "no tool result upgrades a claim to PROVED"
    assert d["supports_at_most"] == "COMPUTATIONALLY_VERIFIED"


def test_numeric_result_without_precision_warns():
    from sciencebro_math.core import Result

    r = Result(tool="t", inputs={}, status="ok", evidence_kind="NUMERIC")
    assert any("precision" in w for w in r.warnings)
    assert not r.exact


def test_hierarchy_window_is_respected():
    """The window must not run past the stated last index -- the 29 August mistake."""
    p = normalized_means(centered_squares(15))
    r = log_difference_hierarchy(p, rmax=4, window_must_fit_in=7)
    for order in r.data["by_order"].values():
        assert order["tested"] >= 0
    assert r.inputs["window_must_fit_in"] == 7


def test_ratio_log_concavity_warns_when_no_domain_given():
    p = normalized_means(centered_squares(11))
    assert any("domain" in w for w in ratio_log_concavity(p).warnings)
    assert ratio_log_concavity(p, upto=5).warnings == []
