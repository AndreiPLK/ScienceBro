
## Night batch 2026-08-15 09:33
- 09:33:45 queue loaded: 3 tasks
- 09:33:45 START 2n8-hunt
- 09:33:46 DONE  2n8-hunt: 2n-8 hunt: 0 alarms over 34 lambdas
- 09:33:46 START lowspin-stress
- 09:33:49 DONE  lowspin-stress: low-spin stress: 0 alarms in 7 checks (depth 20, all even l)
- 09:33:49 START d4-deep120

## Night batch 2026-08-15 13:21
- 13:21:18 queue loaded: 3 tasks
- 13:21:18 START completeness-deep-n80
- 13:21:18 FAIL  completeness-deep-n80: KeyError: 41
- 13:21:18 START closest-approach-exact
- 13:25:11 DONE  closest-approach-exact: closest-approach exact: 24375 checks, 0 alarms
- 13:25:11 START j6-brackets
- 13:27:41 DONE  j6-brackets: j=6 brackets extracted for n=7..9
- 13:27:41 night batch finished

## Night batch 2026-08-15 17:02
- 17:02:48 queue loaded: 4 tasks
- 17:02:48 START knife4-open-region
- 17:02:57 DONE  knife4-open-region: knife4 open region: 250283 checks, 0 alarms
- 17:02:58 START completeness-deep-n80
- 18:10:59 DONE  completeness-deep-n80: deep completeness n<=80: 25002978 checks, 0 alarms
- 18:11:00 START closest-approach-exact
- 18:15:00 DONE  closest-approach-exact: closest-approach exact: 24375 checks, 0 alarms
- 18:15:00 START j6-brackets
- 18:17:43 DONE  j6-brackets: j=6 brackets extracted for n=7..9
- 18:17:43 night batch finished

## Night batch 2026-08-15 19:40
- 19:40:03 queue loaded: 6 tasks
- 19:40:03 START knife4-far-below-variants

## Night batch 2026-08-15 21:59
- 21:59:50 queue loaded: 3 tasks
- 21:59:50 START knife5-belowdiag-factored
- 22:48:35 DONE  knife5-belowdiag-factored: knife5 far-below factored: exit 0: y-coefficients: 5
  c0: OK (2847s)
  c1: OK (2904s)
  c2: OK (2918s)
  c3: OK (2923s)
  c4: OK (2923s)
FAR-BELOW(j=5) CLOSED

- 22:48:35 START knife6-shallow
- 22:54:26 DONE  knife6-shallow: knife6 shallow: exit 0:  (293s)
branch k=39: OK (301s)
branch k=40: OK (309s)
branch k=41: OK (317s)
branch k=42: OK (325s)
branch k=43: OK (333s)
branch k=44: OK (342s)
branch k=45: OK (350s)
SHALLOW CERTIFIED (cells 1591)

- 22:54:26 START knife6-tails
- 00:54:22 FAIL  knife6-tails: subprocess.TimeoutExpired: Command '['C:\\Users\\user\\ScienceBro\\.venv\\Scripts\\python.exe', '-u', 'C:\\Users\\user\\ScienceBro\\projects\\qg-bootstrap\\lab\\knife_tail_deep.py']' timed out after 7200 seconds
- 00:54:23 night batch finished
- 01:04:12 FAIL  knife4-far-below-variants: subprocess.TimeoutExpired: Command '['C:\\Users\\user\\ScienceBro\\.venv\\Scripts\\python.exe', '-u', 'C:\\Users\\user\\ScienceBro\\projects\\qg-bootstrap\\lab\\knife_belowdiag_shift.py']' timed out after 10800 seconds
