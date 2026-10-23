"""Byte-stuffing and bit-stuffing framing helpers."""

FLAG_BYTE = 0x7E
ESCAPE_BYTE = 0x7D
FLAG_BITS = "01111110"

def byte_stuff(payload: bytes) -> bytes:
    """Frame bytes using 0x7E flags and 0x7D escape bytes."""
    out = bytearray([FLAG_BYTE])
    for byte in payload:
        if byte in (FLAG_BYTE, ESCAPE_BYTE):
            out.append(ESCAPE_BYTE)
            out.append(byte ^ 0x20)
        else:
            out.append(byte)
    out.append(FLAG_BYTE)
    return bytes(out)

def byte_unstuff(frame: bytes) -> bytes:
    if len(frame) < 2 or frame[0] != FLAG_BYTE or frame[-1] != FLAG_BYTE:
        raise ValueError("Invalid byte-stuffed frame: missing boundary flag.")
    body = frame[1:-1]
    out = bytearray()
    i = 0
    while i < len(body):
        if body[i] == ESCAPE_BYTE:
            i += 1
            if i >= len(body):
                raise ValueError("Invalid escape sequence.")
            out.append(body[i] ^ 0x20)
        else:
            out.append(body[i])
        i += 1
    return bytes(out)

def bit_stuff(bits: str) -> str:
    """Add flags and insert a 0 after every run of five consecutive 1s."""
    stuffed = []
    ones = 0
    for bit in bits:
        if bit not in "01":
            raise ValueError("Bit string must contain only 0 and 1.")
        stuffed.append(bit)
        if bit == "1":
            ones += 1
            if ones == 5:
                stuffed.append("0")
                ones = 0
        else:
            ones = 0
    return FLAG_BITS + "".join(stuffed) + FLAG_BITS

def bit_unstuff(frame_bits: str) -> str:
    if not frame_bits.startswith(FLAG_BITS) or not frame_bits.endswith(FLAG_BITS):
        raise ValueError("Invalid bit-stuffed frame: missing boundary flag.")
    body = frame_bits[len(FLAG_BITS):-len(FLAG_BITS)]
    out = []
    ones = 0
    i = 0
    while i < len(body):
        bit = body[i]
        if bit not in "01":
            raise ValueError("Bit string must contain only 0 and 1.")
        out.append(bit)
        if bit == "1":
            ones += 1
            if ones == 5:
                # A stuffed zero must follow five consecutive ones.
                i += 1
                if i >= len(body) or body[i] != "0":
                    raise ValueError("Invalid stuffed sequence.")
                ones = 0
        else:
            ones = 0
        i += 1
    return "".join(out)
