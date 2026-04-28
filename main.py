#!/usr/bin/env python3
# Run this to verify the active Python environment can load BCI dependencies.

import sys
import os
from pathlib import Path
from importlib.metadata import PackageNotFoundError, version


PROJECT_ROOT = Path(__file__).resolve().parent
BUNDLED_LIBLSL = PROJECT_ROOT / "liblsl-1.17.7-jammy_amd64" / "lib" / "liblsl.so.1.17.7"

if "PYLSL_LIB" not in os.environ and BUNDLED_LIBLSL.exists():
    os.environ["PYLSL_LIB"] = str(BUNDLED_LIBLSL)

print("🐍 Python executable:", sys.executable)
print("🐍 Python version:", sys.version)
print("🧠 Testing BCI Digital Twin environment...")

# Core imports
# import numpy as np
# print("✅ NumPy:", np.__version__)

# import scipy.signal
# print("✅ SciPy:", scipy.__version__)

try:
    import brainflow
    try:
        brainflow_version = version("brainflow")
    except PackageNotFoundError:
        brainflow_version = "installed"
    print("✅ BrainFlow:", brainflow_version)
except Exception as exc:
    print(f"❌ BrainFlow missing: {exc}")

try:
    import pylsl
    print("✅ PyLSL ready")
except Exception as exc:
    print(f"❌ PyLSL missing: {exc}")
    if not BUNDLED_LIBLSL.exists():
        print(f"   Expected bundled liblsl at: {BUNDLED_LIBLSL}")

# Test digital twin
from digital_twin_bci import DigitalTwinBCI
twin = DigitalTwinBCI()
sample = twin.generate_realistic_eeg()

print("🎯 DIGITAL TWIN EEG SAMPLE:")
print(f"   Channels: {len(sample.eeg)}")
print(f"   C3 (ch2): {sample.eeg[2]:.1f}μV")
print(f"   C4 (ch6): {sample.eeg[6]:.1f}μV")
print(f"   Pz (ch4): {sample.eeg[4]:.1f}μV")
print("🚀 BCI digital twin smoke test complete!")
