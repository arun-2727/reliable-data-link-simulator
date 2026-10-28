"""Byte/special-character restoration and bit-stuffing helpers with traces."""

BYTE_FLAG = "@"
FLAG_BITS = "01111110"


def byte_stuff_trace(message: str) -> dict:
    """Educational reversible mode: remove reserved @ characters and record their positions.

    This custom demonstration is intentionally distinct from conventional byte stuffing,
    which usually escapes reserved bytes rather than deleting them.
    """
    positions = [i for i, char in enumerate(message) if char == BYTE_FLAG]
    payload = "".join(char for char in message if char != BYTE_FLAG)
    frame = BYTE_FLAG + payload + BYTE_FLAG
    steps = []
    for index, char in enumerate(message):
        if char == BYTE_FLAG:
            steps.append({
                "Position": index,
                "Character": char,
                "Operation": "Omit from intermediate payload; record position for restoration",
                "Output": "(not added to payload)",
            })
        else:
            steps.append({
                "Position": index,
                "Character": char,
                "Operation": "Copy unchanged",
                "Output": char,
            })
    return {
        "flag": BYTE_FLAG,
        "original_message": message,
        "stuffed_body": payload,
        "frame": frame,
        "restoration_positions": positions,
        "restoration_character": BYTE_FLAG,
        "steps": steps,
    }


def byte_unstuff_trace(frame: str, positions: list[int]) -> str:
    if len(frame) < 2 or frame[0] != BYTE_FLAG or frame[-1] != BYTE_FLAG:
        raise ValueError("Invalid frame: missing @ boundary flags.")
    payload = frame[1:-1]
    recovered = payload
    for position in positions:
        if position < 0 or position > len(recovered):
            raise ValueError("Invalid restoration position.")
        recovered = recovered[:position] + BYTE_FLAG + recovered[position:]
    return recovered


def bytes_to_bits(data: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in data)


def bit_stuff(bits: str) -> str:
    """Add boundary flags and stuff a zero after every five consecutive ones."""
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


def bit_stuff_trace(bits: str) -> dict:
    stuffed = []
    steps = []
    ones = 0
    inserted_positions = []
    for index, bit in enumerate(bits):
        if bit not in "01":
            raise ValueError("Bit string must contain only 0 and 1.")
        stuffed.append(bit)
        if bit == "1":
            ones += 1
            if ones == 5:
                stuffed.append("0")
                inserted_positions.append(len(stuffed) - 1)
                steps.append({
                    "Input bit position": index,
                    "Operation": "Insert 0 after five consecutive 1s",
                    "Inserted bit": "0",
                })
                ones = 0
        else:
            ones = 0
    body = "".join(stuffed)
    return {
        "flag": FLAG_BITS,
        "original_bits": bits,
        "steps": steps,
        "stuffed_body": body,
        "inserted_positions": inserted_positions,
        "frame": FLAG_BITS + body + FLAG_BITS,
    }


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
                i += 1
                if i >= len(body) or body[i] != "0":
                    raise ValueError("Invalid stuffed sequence.")
                ones = 0
        else:
            ones = 0
        i += 1
    return "".join(out)
