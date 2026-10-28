"""End-to-end simulation of byte/special-character and bit stuffing."""
from framing import byte_stuff_trace, byte_unstuff_trace, bit_stuff_trace, bit_unstuff, bytes_to_bits


def simulate(message: str, framing: str = "Byte stuffing") -> dict:
    if not message:
        raise ValueError("Please enter a message to transmit.")
    payload = message.encode("utf-8")
    if framing == "Byte stuffing":
        trace = byte_stuff_trace(message)
        recovered = byte_unstuff_trace(trace["frame"], trace["restoration_positions"])
        return {
            "framing": framing,
            "message": message,
            "trace": trace,
            "recovered_message": recovered,
            "original_bytes": " ".join(f"{b:02X}" for b in payload),
        }
    if framing == "Bit stuffing":
        original_bits = bytes_to_bits(payload)
        trace = bit_stuff_trace(original_bits)
        recovered_bits = bit_unstuff(trace["frame"])
        recovered_bytes = bytes(int(recovered_bits[i:i + 8], 2) for i in range(0, len(recovered_bits), 8))
        recovered = recovered_bytes.decode("utf-8")
        return {
            "framing": framing,
            "message": message,
            "trace": trace,
            "recovered_message": recovered,
            "original_bytes": " ".join(f"{b:02X}" for b in payload),
            "original_bits": original_bits,
        }
    raise ValueError("Choose Byte stuffing or Bit stuffing.")
