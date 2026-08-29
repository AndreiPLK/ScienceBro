# Total positivity and the hierarchy are complementary — the normalisation creates one and destroys the other

*2026-08-29 night, found with the new `sciencebro-math` battery. Exact throughout.*

## The table

| sequence | Toeplitz minors (Pólya frequency) | `Delta^r log` hierarchy |
|---|---|---|
| raw `e_t` of the centred spectrum | **holds** | **fails** |
| normalised `p_t = e_t / C(N,t)` | **fails** | **holds** |

Tested at `n = 11, 15, 21`; the pattern is identical at each, on the full sequence and
on the first half alike.

## Why this is not a bug

`e_t` is the coefficient sequence of `prod (1 + b_k z)` with all `b_k > 0`, so the
polynomial is real-rooted with negative roots and Aissen–Schoenberg–Whitney says the
coefficient sequence **must** be a Pólya frequency sequence. It is: every Toeplitz
minor to order 3 is nonnegative. That is the positive control, and it passing is what
makes the negative result on `p` trustworthy rather than a coding accident.

The failure on `p` is explicit and exact, not marginal:

    n = 11:  rows (1,2,3), cols (0,1,2):  det = -40832/15
    n = 15:  same position:               det = -106240/7
    n = 21:  same position:               det = -1384592/15

The same minor position fails at every `n`, which is the signature of a structural
obstruction rather than a boundary artefact.

## What it means for the programme

The binomial normalisation is not cosmetic. **It destroys total positivity and creates
the log-difference hierarchy.** The two properties do not merely fail to coincide; they
sit on opposite sides of the same division.

That closes a route which was, until tonight, the leading surviving candidate. A
Lindström–Gessel–Viennot or planar-network argument works on the totally positive
object — and the totally positive object is `e`, which does **not** have the hierarchy.
Whatever explains the hierarchy has to be a statement about `e_t / C(N,t)` as such,
about the interaction between the spectrum and the binomial weights, and not about
either factor alone.

Combined with `MOMENT_ROUTE_REFUTED.md`, both mechanisms proposed for the hierarchy are
now excluded:

* a positive-measure representation — refuted, both orientations;
* total positivity of the sequence carrying the hierarchy — refuted, exactly.

## What survives

* a determinant or minor identity for `H_{N,t}` **after** clearing the binomial
  denominators, which is a different object from the Toeplitz array of `p`;
* a recurrence carrying the sign;
* the finite free / S-transform curvature reading, which lives naturally in normalised
  coordinates and is therefore on the right side of the division;
* an as-yet-unnamed mechanism specific to the pairing of a real-rooted spectrum with
  binomial weights.

The last is where I would look. The division found here says the phenomenon belongs to
the normalisation, and normalised elementary means are exactly the coordinates of the
finite free transforms.

## A correction to my own record

An earlier draft of tonight's journal listed "Toeplitz minors of `p` pass everywhere
tested" as an anomaly. That was written from the shape of the scanner rather than from
a measurement, and it is false. Corrected in `research/journal/2026-08-29.md`. The
error is exactly the kind the new claim registry and completion audit exist to catch,
and it is worth recording that the system caught it within the hour.
