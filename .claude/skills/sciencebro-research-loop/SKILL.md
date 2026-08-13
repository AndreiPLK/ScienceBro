---
name: sciencebro-research-loop
description: Enforce rapid, evidence-producing scientific iterations for all ScienceBro research. Always use before planning research, estimating duration, reading papers, reproducing results, generating hypotheses, building research infrastructure, running experiments, proving claims, or declaring novelty.
---

# ScienceBro Research Loop

## Purpose

Maximize verified scientific knowledge produced per iteration.

The North Star remains unchanged:
Derive unavoidable properties of quantum gravity from consistency principles and determine,
within explicit assumptions, whether consistent quantum gravity must become string-like or
whether genuine alternatives exist.

Plans, tools, dashboards and code have zero value unless they directly change what we
scientifically know.

## 1. Work in vertical slices

Never begin with a large roadmap.
Choose the smallest end-to-end question that can produce evidence now:
`precise claim → minimal test → result → adversarial check → next claim`

Each iteration must end with at least one concrete scientific artifact:

* reproduced equation, table, figure or theorem;
* numerical result;
* symbolic derivation;
* tested counterexample;
* falsified candidate;
* rigorous citation;
* proof fragment;
* explicit knowledge gap.

A plan alone is never a completed iteration.

## 2. Start each iteration in seven lines or fewer

State:

1. Exact question or claim.
2. Why it advances the North Star.
3. Smallest decisive test.
4. Falsification or kill criterion.
5. Artifact that will exist afterward.
6. Required dependency, if any.
7. Measured execution estimate.

Then execute immediately.
Do not respond with another roadmap unless the user explicitly requests one.

## 3. Honest time calibration

Never estimate "days", "weeks" or "months" from intuition, academic tradition or human-only
workflows. For unfamiliar work, first run the smallest useful calibration experiment.
Estimate the remaining work only after observing actual throughput.

Always separate:

* `AGENT_EXECUTION_TIME`: active Claude/computer work;
* `ANDREY_TIME`: optional reading, understanding or decisions required from Andrey;
* `EXTERNAL_WAIT_TIME`: reviewers, APIs, endorsements or other dependencies.

Record predicted versus actual active execution time for every iteration in one compact
existing mission log. Do not build a new tracking platform.

After three completed iterations:

1. Calculate the prediction error.
2. Recalibrate future estimates from observed throughput.
3. Immediately shorten estimates when evidence shows faster execution.
4. Explain the assumptions behind any estimate.

If there is no empirical basis, say:
`UNKNOWN — running a calibration slice now.`

Complexity is not a duration. Never convert "hard mathematics" automatically into
"several weeks".

## 4. Science before infrastructure

At least 80% of completed actions must directly examine physics or mathematics.
Infrastructure is allowed only when all are true:

* the current scientific test is blocked without it;
* an existing tool cannot do the job;
* the tool will be used in the current iteration;
* its output has a deterministic scientific test;
* it is the smallest possible implementation.

Stop immediately if building infrastructure consumes two consecutive iterations without
producing scientific evidence. Do not build speculative platforms "for later".

## 5. Idea honesty

An LLM-generated idea is only an `IDEA`.
For every idea, state:

* exact mathematical claim;
* assumptions;
* why it might be true;
* fastest way to prove it false;
* current evidence;
* what evidence is missing;
* novelty status.

Track evidence status and novelty separately.
Allowed novelty statuses:

* `NOVELTY_UNCHECKED`
* `POSSIBLY_KNOWN`
* `LITERATURE_SEARCHED`
* `NOVELTY_CONFIRMED_BY_EXPERT`

Never call an idea "new", "breakthrough", "publishable", "strong" or "important" merely
because it sounds plausible or survived several numerical tests.
Search for counterexamples before trying to defend an idea.

## 6. Progressive difficulty

Do not attempt the grand theorem directly. Grow through this ladder:

1. Reproduce one known result.
2. Change one assumption.
3. Observe exactly what breaks.
4. Formulate the smallest surviving claim.
5. Attack it numerically and symbolically.
6. Prove it analytically.
7. Formalize only the valuable proof core.
8. Check novelty and physical meaning.

Every iteration must leave the next iteration more informed and narrower.

## 7. Failure and pivot rules

* One failed candidate is useful evidence.
* Two iterations without new evidence: shrink the question.
* Three iterations without new evidence: kill or replace the microproblem.
* Never keep a task alive because substantial code was already written.
* Preserve failures, but do not decorate them into achievements.

## 8. Self-improvement

After every iteration, record only:

* prediction versus actual;
* what assumption was wrong;
* what method worked;
* what should change next time.

After five iterations, compress repeated lessons into one improved rule. Remove obsolete
rules instead of endlessly appending text. Do not modify the North Star. Improve only
execution and calibration.

## 9. Required checkpoint format

Report briefly:

* `RESULT:` what was actually produced;
* `EVIDENCE:` exact artifact or test;
* `STATUS:` existing ScienceBro truth level;
* `NOVELTY:` separate novelty status;
* `TIME:` predicted versus actual agent time;
* `LEARNED:` what changed in our understanding;
* `NEXT:` one smallest decisive experiment.

Never report activity as progress. Report only changed knowledge.
