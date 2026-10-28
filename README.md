# Interactive Data Link Layer Framing Simulator

A Computer Networks CBP project that demonstrates byte/special-character restoration and bit stuffing with readable, step-by-step output.

## Features
- Choose byte/special-character mode or bit stuffing
- Display the flag used by each method (`@` for the custom byte-mode demonstration and `01111110` for bit stuffing)
- Show intermediate results as readable text or binary, not hex by default
- Show character/bit-level operations
- Restore the original message and verify the round trip
- Optional hexadecimal view for byte-level debugging
- Automated tests using pytest

## Important note about the byte-mode demonstration
To match the instructor's example, the app demonstrates `hello@world` becoming `helloworld` as the intermediate payload, then restoring `hello@world` at the receiver. It records the omitted `@` character's original position as restoration metadata. The receiver needs that metadata because `helloworld` alone does not reveal where an `@` was removed.

This remove-and-restore approach is a **custom educational reversible scheme**, not conventional byte stuffing. Conventional byte stuffing typically escapes a reserved byte rather than removing it.

## Bit stuffing
The bit-stuffing mode uses the HDLC-style flag `01111110`. It inserts a `0` after every five consecutive `1` bits in the data body, and the receiver removes the inserted zeros.

## Requirements
Python 3.10 or newer is recommended.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Run the dashboard
```powershell
py -m streamlit run app.py
```

## Run tests
```powershell
py -m pytest -q
```

## Demo suggestions
- Byte mode: enter `hello@world`; expected intermediate payload is `helloworld`, with `@` at position `5` recorded for restoration.
- Bit mode: enter a message and inspect the binary representation, stuffed bits, flags, and receiver output.

## Scope
This is a software simulation. It does not transmit data over a real network and does not implement CRC.
