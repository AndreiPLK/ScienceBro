# Independence statement

The verifier package (projects/ainstein-audit/verifier/) imports no upstream code; exported metric values cross the boundary as plain float64 arrays via a subprocess in an isolated environment. Verified by inspection of imports and by construction of the interface (verifier/interface.py).
