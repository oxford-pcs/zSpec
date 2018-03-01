# zSpec
Programmatically assemble a spectrograph from Zemax files using PyZDDE.

## Dependencies
- Zemax
- PyZDDE
- zController

## Overview
This package allows the user to assemble a spectrograph from separate optical design files (Zemax) for the collimator and camera by instantiating the Spectrograph() class. 

## Current Capabilities
- calculateMagnification() - calculate magnification of system
- doSystemRayTrace() - perform raytrace through system
- getSystemWFE() - get the total system WFE

