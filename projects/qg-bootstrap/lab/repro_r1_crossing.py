"""R1: derive the closed forms of arXiv:2406.02665 Eqs. (11)-(13) from crossing.

Independent derivation, sharing no algebra with the paper beyond the setup:
  A(s,t) = sum_n c(n) * prod_{k=1..n} (t - xi(k)) / (mu(n) - s)      (Eqs. 3+7)
  gauge:  mu(0)=0, mu(1)=1, c(0)=1                                    (p.2)
  level truncation: at t = xi(j) only levels n < j contribute
  crossing at truncation points: A(xi(i), xi(j)) = A(xi(j), xi(i))    (Eq. 10)

We build the crossing equations symbolically with SymPy, solve them SEQUENTIALLY
(i=1 -> c(n); i=2 -> mu(n); i=3 -> xi(n)), and compare against the paper's closed
forms:
  (11) c(n)  = (-1)^n (xi(1) - mu(n)) / prod_{k=1..n+1} xi(k)
  (12) mu(n) = [mu(n-1)(xi(n+1) - 1) + xi(2)] / xi(n+1)
  (13) xi(n) = xi(3) (xi(n-1) - 1) / (xi(2) - 1)

Every check prints PASS/FAIL; exit code 1 on any FAIL. Pure symbols — no floats.
"""

from __future__ import annotations

import os
import sys

import sympy as sp

N = int(os.environ.get("R1_N", "7"))


def truncated_amplitude(s_val, t_is_xi_j: int, c, mu, xi):
    """A(s, xi(j)) via level truncation: only n < j contribute."""
    j = t_is_xi_j
    total = 0
    for n in range(j):
        res = c[n]
        for k in range(1, n + 1):
            res *= xi[j] - xi[k]
        total += res / (mu[n] - s_val)
    return total


def main() -> int:
    c = {n: sp.Symbol(f"c{n}") for n in range(N)}
    mu = {n: sp.Symbol(f"mu{n}") for n in range(N)}
    xi = {k: sp.Symbol(f"xi{k}") for k in range(1, N + 2)}

    # gauge fixing (paper p.2)
    c[0] = sp.Integer(1)
    mu[0] = sp.Integer(0)
    mu[1] = sp.Integer(1)

    failures = 0

    def crossing_eq(i: int, j: int):
        lhs = truncated_amplitude(xi[i], j, c, mu, xi)
        rhs = truncated_amplitude(xi[j], i, c, mu, xi)
        return sp.together(lhs - rhs)

    # ---- Step 1: i=1, j>=2 determines c(n) --------------------------------
    # Paper Eq. (11). Solve sequentially in j.
    c_solved = {0: sp.Integer(1)}
    for j in range(2, N):
        eq = crossing_eq(1, j)
        # substitute previously solved c's
        eq = eq.subs({c[n]: c_solved[n] for n in range(j - 1) if n in c_solved})
        sol = sp.solve(sp.numer(eq), c[j - 1])
        if len(sol) != 1:
            print(f"FAIL step1 j={j}: expected unique solution, got {len(sol)}")
            return 1
        c_solved[j - 1] = sp.simplify(sol[0])

    def c_paper(n: int):
        expr = (-1) ** n * (xi[1] - mu[n])
        for k in range(1, n + 2):
            expr /= xi[k]
        return expr

    for n in range(1, N - 1):
        diff = sp.simplify(c_solved[n] - c_paper(n))
        ok = diff == 0
        print(f"R1a c({n}) matches Eq.(11): {'PASS' if ok else 'FAIL: ' + str(diff)}")
        failures += 0 if ok else 1

    # ---- Step 2: i=2, j>=3 determines mu(n) --------------------------------
    # Substitute c(n) closed form, solve crossing for mu(j-1) sequentially.
    subs_c = {c[n]: c_paper(n) for n in range(1, N - 1)}
    mu_solved = {}
    prev_mu = {0: sp.Integer(0), 1: sp.Integer(1)}
    for j in range(3, N):
        eq = crossing_eq(2, j).subs(subs_c)
        eq = eq.subs({mu[n]: prev_mu[n] for n in prev_mu if n >= 2})
        sol = sp.solve(sp.numer(eq), mu[j - 1])
        if len(sol) != 1:
            print(f"FAIL step2 j={j}: {len(sol)} solutions")
            return 1
        mu_solved[j - 1] = sp.simplify(sol[0])
        prev_mu[j - 1] = mu_solved[j - 1]

    # Compare against recursion Eq. (12): mu(n) = [mu(n-1)(xi(n+1)-1)+xi(2)]/xi(n+1)
    mu_rec = {0: sp.Integer(0), 1: sp.Integer(1)}
    for n in range(2, N - 1):
        mu_rec[n] = sp.simplify((mu_rec[n - 1] * (xi[n + 1] - 1) + xi[2]) / xi[n + 1])
    for n in range(2, N - 1):
        diff = sp.simplify(mu_solved[n] - mu_rec[n])
        ok = diff == 0
        print(f"R1b mu({n}) matches Eq.(12): {'PASS' if ok else 'FAIL: ' + str(diff)}")
        failures += 0 if ok else 1

    # ---- Step 3: i=3, j>=4 determines xi(n) --------------------------------
    subs_mu = {mu[n]: mu_rec[n] for n in range(2, N - 1)}
    xi_constraints = []
    for j in range(4, N):
        eq = crossing_eq(3, j).subs(subs_c).subs(subs_mu)
        eq = sp.simplify(sp.numer(sp.together(eq)))
        xi_constraints.append((j, eq))

    # Paper Eq. (13): xi(n) = xi(3)(xi(n-1)-1)/(xi(2)-1). Verify each constraint
    # vanishes on that recursion (checking the recursion SOLVES the equations).
    xi_rec = {1: xi[1], 2: xi[2], 3: xi[3]}
    for n in range(4, N + 1):
        xi_rec[n] = sp.simplify(xi[3] * (xi_rec[n - 1] - 1) / (xi[2] - 1))
    for j, eq in xi_constraints:
        val = sp.simplify(eq.subs({xi[k]: xi_rec[k] for k in range(4, N + 1)}))
        ok = val == 0
        print(
            f"R1c crossing(3,{j}) vanishes on Eq.(13) recursion: "
            f"{'PASS' if ok else 'FAIL: ' + str(val)[:120]}"
        )
        failures += 0 if ok else 1

    print(f"\nR1 verdict: {'ALL PASS' if failures == 0 else f'{failures} FAILURES'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
