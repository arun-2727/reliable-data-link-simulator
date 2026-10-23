"""End-to-end data-link simulation orchestration."""
from crc import append_crc, bytes_to_bits, bits_to_bytes, verify_codeword
from framing import byte_stuff, byte_unstuff, bit_stuff, bit_unstuff
from channel import flip_bit

def simulate(message: str, framing: str = "Byte stuffing",
             inject_error: bool = False, error_bit_index: int = 0,
             frame_size: int = 8) -> dict:
    if not message:
        raise ValueError("Please enter a message to transmit.")
    if frame_size < 1:
        raise ValueError("Frame size must be at least 1 byte.")

    raw = message.encode("utf-8")
    chunks = [raw[i:i+frame_size] for i in range(0, len(raw), frame_size)]
    results = []
    for frame_no, chunk in enumerate(chunks, start=1):
        codeword = append_crc(chunk)
        codeword_bits = bytes_to_bits(codeword)
        if framing == "Byte stuffing":
            wire = byte_stuff(codeword)
            # For consistent, safe demo behavior, corruption is applied to the
            # codeword before framing, so delimiters cannot accidentally vanish.
            if inject_error and frame_no == 1:
                corrupted_bits = flip_bit(codeword_bits, error_bit_index)
                received_codeword = bits_to_bytes(corrupted_bits)
                wire_received = byte_stuff(received_codeword)
            else:
                received_codeword = codeword
                wire_received = wire
            decoded = byte_unstuff(wire_received)
            wire_display = wire.hex(" ").upper()
            received_wire_display = wire_received.hex(" ").upper()
        elif framing == "Bit stuffing":
            wire = bit_stuff(codeword_bits)
            if inject_error and frame_no == 1:
                corrupted_bits = flip_bit(codeword_bits, error_bit_index)
                received_codeword = bits_to_bytes(corrupted_bits)
                wire_received = bit_stuff(bytes_to_bits(received_codeword))
            else:
                received_codeword = codeword
                wire_received = wire
            decoded_bits = bit_unstuff(wire_received)
            decoded = bits_to_bytes(decoded_bits)
            wire_display = wire
            received_wire_display = wire_received
        else:
            raise ValueError("Unsupported framing method.")

        valid = verify_codeword(decoded)
        data_part = decoded[:-1] if len(decoded) >= 1 else b""
        try:
            decoded_text = data_part.decode("utf-8") if valid else ""
        except UnicodeDecodeError:
            decoded_text = "[Invalid UTF-8]"
        results.append({
            "frame": frame_no,
            "original_data": chunk.decode("utf-8", errors="replace"),
            "data_hex": chunk.hex(" ").upper(),
            "crc": f"{codeword[-1]:08b}",
            "codeword_bits": codeword_bits,
            "wire_sent": wire_display,
            "wire_received": received_wire_display,
            "received_codeword_bits": bytes_to_bits(decoded),
            "remainder": f"{0 if valid else 1:08b}" if valid else "NON-ZERO (error detected)",
            "valid": valid,
            "decoded_text": decoded_text,
            "error_injected": bool(inject_error and frame_no == 1),
        })

    accepted = [r for r in results if r["valid"]]
    recovered = "".join(r["decoded_text"] for r in accepted)
    return {
        "message": message,
        "framing": framing,
        "frames": results,
        "total_frames": len(results),
        "accepted_frames": len(accepted),
        "rejected_frames": len(results) - len(accepted),
        "success_rate": (len(accepted) / len(results) * 100) if results else 0,
        "recovered_message": recovered,
    }
