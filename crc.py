"""CRC-8 implementation using generator polynomial x^8 + x^2 + x + 1 (0x07)."""

def bytes_to_bits(data: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in data)

def bits_to_bytes(bits: str) -> bytes:
    if len(bits) % 8:
        raise ValueError("Bit string length must be a multiple of 8.")
    if any(bit not in "01" for bit in bits):
        raise ValueError("Bit string must contain only 0 and 1.")
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def crc_remainder(data: bytes, polynomial: int = 0x07) -> int:
    """Return the 8-bit CRC remainder for data using CRC-8 polynomial 0x07."""
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ polynomial) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

def append_crc(data: bytes) -> bytes:
    return data + bytes([crc_remainder(data)])

def verify_codeword(codeword: bytes) -> bool:
    """For this CRC-8 convention, a valid codeword has zero remainder."""
    return crc_remainder(codeword) == 0
