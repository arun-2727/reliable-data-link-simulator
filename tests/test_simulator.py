import pytest
from crc import append_crc, verify_codeword
from framing import byte_stuff, byte_unstuff, bit_stuff, bit_unstuff
from simulator import simulate

def test_crc_valid_codeword():
    codeword = append_crc(b"hello")
    assert verify_codeword(codeword)

def test_crc_detects_single_bit_flip():
    codeword = bytearray(append_crc(b"hello"))
    codeword[0] ^= 0x01
    assert not verify_codeword(bytes(codeword))

def test_byte_stuff_round_trip_special_bytes():
    data = bytes([0x00, 0x7E, 0x7D, 0x41])
    assert byte_unstuff(byte_stuff(data)) == data

def test_bit_stuff_round_trip():
    data = "0111111011111100"
    assert bit_unstuff(bit_stuff(data)) == data

def test_clean_simulation():
    result = simulate("hello world", frame_size=5)
    assert result["rejected_frames"] == 0
    assert result["recovered_message"] == "hello world"

def test_corrupted_simulation_rejects_first_frame():
    result = simulate("hello world", inject_error=True, error_bit_index=0, frame_size=5)
    assert result["rejected_frames"] == 1
    assert result["accepted_frames"] >= 1

def test_empty_message_rejected():
    with pytest.raises(ValueError):
        simulate("")
