# zSpec
Programmatically assemble a spectrograph from Zemax files using PyZDDE.

# Dependencies
- PyZDDE
- zController

# Overview
The classes contain herein allow the user to assemble a spectrograph from Zemax optical designs for the collimator and camera.

Once assembled, the system can be fully raytraced for any field(s) from the entrance slit to the image plane. Functions to assemble 
an entrance slit are included (such as the "brick wall" pattern from SWIFT).

Slit "patterns" and detectors can be added to the `slits.json` and `detectors.json` files respectively, but if adding a new 
type of pattern the corresponding logic to decompose it into field points must be added to the `getFieldsFromSlitPattern()` function 
in `slit.py`.

# Usage

Example usages are shown in the test scripts `test_doRayTrace.py` and `test_getWFE.py`.
