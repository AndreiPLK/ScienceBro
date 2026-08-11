#!/bin/bash
# GPU environment for the AInstein upstream runs inside WSL Ubuntu.
# TF 2.21 pip nvidia wheels need every nvidia/*/lib dir on LD_LIBRARY_PATH
# (libcusolver.so.11 fails to dlopen its deps otherwise — verified 2026-08-11).
PY=/opt/gpu312/bin/python
NVLIBS=$($PY - <<'EOF'
import glob, os, nvidia
print(":".join(glob.glob(os.path.join(os.path.dirname(nvidia.__file__), "*", "lib"))))
EOF
)
export LD_LIBRARY_PATH="$NVLIBS:$LD_LIBRARY_PATH"
exec $PY "$@"
