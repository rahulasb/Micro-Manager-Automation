Green/Blue Laser Backend

Requirements:
- Windows PC
- Micro-Manager running
- Pycro-Manager server enabled on port 4827
- Python 3.13
- pycromanager installed

Micro-Manager device names:
- Green_Sapphire
- Blue_Sapphire

Verified hardware mapping:
- Green Sapphire: COM7, 561 nm
- Blue Sapphire: COM6, 488 nm

State property:
- "1" = ON
- "0" = OFF

PowerSetpoint ranges:
- Green: 20 to 220
- Blue: 15 to 165

Important:
State values must be sent as strings:
"1"
"0"

Main backend file:
laser_backend.py

Main high-level function:
laser.configure(
    mode="GREEN_ONLY",
    green_power=50,
    blue_power=40
)

Supported modes:
GREEN_ONLY
BLUE_ONLY
ALL_ON
ALL_OFF

The backend:
1. Sets Green power
2. Sets Blue power
3. Sets requested laser states
4. Reads the actual states back
5. Returns LASER_READY = TRUE only when verification succeeds

Run manual test:
python test_lasers.py

Current architecture:
Python
→ Pycro-Manager
→ Micro-Manager Core
→ Sapphire adapter
→ Green/Blue controllers