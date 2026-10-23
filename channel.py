"""Deterministic bit-error injection helpers."""

def flip_bit(bits: str, index: int) -> str:
    """Flip a bit at zero-based index in a binary string."""
    if not bits or any(b not in "01" for b in bits):
        raise ValueError("Input must be a non-empty binary string.")
    if index < 0 or index >= len(bits):
        raise IndexError("Bit index is outside the transmitted bit string.")
    replacement = "1" if bits[index] == "0" else "0"
    return bits[:index] + replacement + bits[index + 1:]
