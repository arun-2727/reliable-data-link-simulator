# Reliable Data Link Transmission Simulator Using Framing and CRC

A Computer Networks CBP project that demonstrates data-link framing, CRC-8 error detection, simulated transmission errors, and receiver-side frame validation.

## Features
- Byte stuffing and bit stuffing
- CRC-8 using polynomial `0x07` (`x^8 + x^2 + x + 1`)
- Configurable payload size per frame
- Optional deterministic bit-error injection into the first frame's data+CRC codeword
- Frame-by-frame sender/receiver inspection
- Summary metrics and receiver output
- Automated tests using pytest

## Requirements
Python 3.10 or newer is recommended.

## Setup (Windows PowerShell)
```powershell
cd reliable-data-link-simulator
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the dashboard
```powershell
streamlit run app.py
```
Streamlit will print a local URL, typically `http://localhost:8501`.

## Run tests
```powershell
python -m pytest -q
```

## How to demo
1. Enter `HELLO NETWORK` and keep error injection disabled.
2. Transmit and show all frames pass CRC.
3. Enable error injection and flip bit index `0`.
4. Transmit again and show the first frame fails CRC while intact frames pass.
5. Switch between byte stuffing and bit stuffing and compare the framed wire representation.
6. Change payload bytes per frame to show how the message is segmented.

## Important implementation note
For a safe, easy-to-understand demonstration, this version applies the injected bit flip to the data+CRC codeword before the framing encoder runs. This preserves frame delimiters and isolates CRC error detection from framing-boundary corruption. A real physical channel usually corrupts the serialized framed bitstream; that is a useful future extension.

## Limitations
- CRC is error detection, not error correction.
- CRC cannot detect every possible multi-bit corruption pattern.
- The summary's accepted frame rate is the fraction of frames passing CRC, not a real network throughput measurement.
- UTF-8 characters may occupy multiple bytes; frame size is measured in bytes.
