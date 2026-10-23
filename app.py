import streamlit as st
import pandas as pd
from simulator import simulate

st.set_page_config(page_title="Reliable Data Link Simulator", page_icon="📡", layout="wide")
st.title("📡 Reliable Data Link Transmission Simulator")
st.caption("Computer Networks CBP • Framing + CRC-8 + simulated transmission errors")

with st.sidebar:
    st.header("Transmission settings")
    framing = st.selectbox("Framing technique", ["Byte stuffing", "Bit stuffing"])
    frame_size = st.slider("Payload per frame (bytes)", min_value=1, max_value=32, value=8)
    inject_error = st.checkbox("Inject a bit error in the first frame", value=False)
    error_bit_index = st.number_input(
        "Bit index to flip in first codeword (0-based)",
        min_value=0, max_value=frame_size * 8 + 7, value=0, step=1,
        help="Index is applied to the first frame's data+CRC codeword before framing. The framing flags remain intact."
    )

message = st.text_area("Message to transmit", value="Reliable data link transmission!", height=100)
st.info("CRC-8 uses generator polynomial x⁸ + x² + x + 1 (0x07). A valid received codeword has a zero CRC remainder.")

if st.button("Transmit message", type="primary", use_container_width=True):
    try:
        result = simulate(message, framing, inject_error, int(error_bit_index), frame_size)
        st.session_state["simulation_result"] = result
    except Exception as exc:
        st.error(str(exc))

result = st.session_state.get("simulation_result")
if result:
    st.subheader("Transmission summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total frames", result["total_frames"])
    c2.metric("Accepted", result["accepted_frames"])
    c3.metric("Rejected", result["rejected_frames"])
    c4.metric("Accepted frame rate", f'{result["success_rate"]:.1f}%')

    if result["rejected_frames"]:
        st.error("At least one frame failed CRC validation. The receiver rejected the corrupted frame.")
    else:
        st.success("All received frames passed CRC validation.")

    st.subheader("Frame-by-frame inspection")
    table = []
    for f in result["frames"]:
        table.append({
            "Frame": f["frame"],
            "Payload": f["original_data"],
            "CRC bits": f["crc"],
            "CRC check": "PASS" if f["valid"] else "FAIL",
            "Error injected": "Yes" if f["error_injected"] else "No",
            "Received data": f["decoded_text"] if f["valid"] else "Rejected",
        })
    st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

    selected = st.selectbox("Inspect frame", [f["frame"] for f in result["frames"]])
    frame = result["frames"][selected - 1]
    left, right = st.columns(2)
    with left:
        st.markdown("#### Sender")
        st.write("Payload (hex)")
        st.code(frame["data_hex"] or "(empty)")
        st.write("Codeword bits (data + CRC)")
        st.code(frame["codeword_bits"])
        st.write("Framed transmission")
        st.code(frame["wire_sent"])
    with right:
        st.markdown("#### Receiver")
        st.write("Received framed transmission")
        st.code(frame["wire_received"])
        st.write("Decoded codeword bits")
        st.code(frame["received_codeword_bits"])
        st.write("CRC verification")
        st.code("PASS — zero remainder" if frame["valid"] else "FAIL — corrupted codeword rejected")

    st.subheader("Receiver output")
    st.code(result["recovered_message"] if result["recovered_message"] else "(No valid frames to recover)")
    st.caption("The receiver output includes only frames that pass CRC. CRC detects many transmission errors but cannot guarantee detection of every possible error pattern.")
