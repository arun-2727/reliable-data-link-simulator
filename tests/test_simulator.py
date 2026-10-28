import pytest
from framing import byte_stuff_trace, byte_unstuff_trace, bit_stuff, bit_unstuff, bit_stuff_trace
from simulator import simulate


def test_custom_byte_mode_restores_single_at_sign():
    result = simulate("hello@world", "Byte stuffing")
    assert result["trace"]["stuffed_body"] == "helloworld"
    assert result["recovered_message"] == "hello@world"
    assert result["trace"]["flag"] == "@"


def test_custom_byte_mode_restores_multiple_at_signs():
    result = simulate("a@b@@c", "Byte stuffing")
    assert result["trace"]["stuffed_body"] == "abc"
    assert result["recovered_message"] == "a@b@@c"


def test_custom_byte_mode_without_at_sign():
    result = simulate("hello world", "Byte stuffing")
    assert result["trace"]["stuffed_body"] == "hello world"
    assert result["recovered_message"] == "hello world"


def test_byte_unstuff_rejects_missing_flags():
    with pytest.raises(ValueError):
        byte_unstuff_trace("helloworld", [5])


def test_bit_stuff_round_trip():
    data = "0111111011111100"
    assert bit_unstuff(bit_stuff(data)) == data


def test_bit_stuff_trace_records_insertions():
    trace = bit_stuff_trace("01111110")
    assert trace["stuffed_body"] == "011111010"
    assert len(trace["steps"]) == 1
    assert trace["flag"] == "01111110"


def test_byte_stuff_simulation_recovers_unicode_message():
    result = simulate("Hello 🌍", "Byte stuffing")
    assert result["recovered_message"] == "Hello 🌍"


def test_bit_stuff_simulation_recovers_unicode_message():
    result = simulate("Hello 🌍", "Bit stuffing")
    assert result["recovered_message"] == "Hello 🌍"


def test_empty_message_rejected():
    with pytest.raises(ValueError):
        simulate("")


def test_invalid_framing_rejected():
    with pytest.raises(ValueError):
        simulate("hello", "CRC")
