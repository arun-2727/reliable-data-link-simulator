import pandas as pd
import streamlit as st
from simulator import simulate


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="FrameLab | Data Link Simulator",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE + CALLBACKS
# ============================================================
def sample_for_mode(mode: str) -> str:
    return "hello@world" if mode == "Byte stuffing" else "A~B}C"


def load_sample() -> None:
    """Button callback: runs before Streamlit rebuilds the widgets."""
    mode = st.session_state.get("framing_mode", "Byte stuffing")
    st.session_state["message_input"] = sample_for_mode(mode)
    st.session_state["framing_result"] = None
    st.session_state["last_run_message"] = None
    st.session_state["last_run_framing"] = None
    st.session_state["simulation_error"] = None


if "framing_mode" not in st.session_state:
    st.session_state["framing_mode"] = "Byte stuffing"
if "message_input" not in st.session_state:
    st.session_state["message_input"] = "hello@world"
if "framing_result" not in st.session_state:
    st.session_state["framing_result"] = None
if "last_run_message" not in st.session_state:
    st.session_state["last_run_message"] = None
if "last_run_framing" not in st.session_state:
    st.session_state["last_run_framing"] = None
if "simulation_error" not in st.session_state:
    st.session_state["simulation_error"] = None


# ============================================================
# CUSTOM DESIGN SYSTEM
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #080d19;
        --panel: #101827;
        --border: rgba(148, 163, 184, .17);
        --text: #edf4ff;
        --muted: #9aa9c1;
        --cyan: #56e0e9;
        --violet: #a78bfa;
        --green: #57e6a7;
    }
    .stApp {
        background: radial-gradient(ellipse at 0% 0%, rgba(55,93,175,.16), transparent 36%),
                    radial-gradient(ellipse at 100% 10%, rgba(133,82,204,.12), transparent 32%),
                    var(--bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stHeader"] { background: rgba(8,13,25,.72); }
    .block-container { max-width: 1450px; padding-top: 1.7rem; padding-bottom: 3.5rem; }
    #MainMenu, footer { visibility: hidden; }
    h1,h2,h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.035em; color: var(--text); }
    p,li,label { color: #c5d0e2; }

    .topbar { display:flex; justify-content:space-between; align-items:center; gap:14px; padding:2px 0 24px; border-bottom:1px solid var(--border); margin-bottom:28px; }
    .brand { display:flex; align-items:center; gap:12px; color:#f4f7ff; font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.15rem; }
    .brand-icon { display:flex; align-items:center; justify-content:center; width:43px; height:43px; border-radius:14px; background:linear-gradient(135deg,#173f59,#273061); border:1px solid rgba(86,224,233,.35); font-size:22px; }
    .brand-sub { display:block; color:var(--muted); font-family:'DM Sans',sans-serif; font-size:.7rem; font-weight:600; letter-spacing:.09em; margin-top:3px; }
    .top-pill { display:inline-flex; gap:8px; align-items:center; border:1px solid rgba(87,230,167,.25); background:rgba(87,230,167,.07); border-radius:99px; padding:8px 13px; color:#9df0c8; font-size:.73rem; font-weight:700; white-space:nowrap; }
    .status-dot { display:inline-block; width:7px; height:7px; border-radius:50%; background:var(--green); box-shadow:0 0 10px rgba(87,230,167,.6); }

    .hero { position:relative; overflow:hidden; padding:clamp(23px,4vw,38px); border-radius:25px; border:1px solid rgba(148,163,184,.19); background:radial-gradient(ellipse at 95% 8%,rgba(167,139,250,.19),transparent 35%),radial-gradient(ellipse at 5% 100%,rgba(86,224,233,.11),transparent 40%),linear-gradient(130deg,#111b2d,#101526 60%,#171329); margin-bottom:28px; }
    .hero-eyebrow { color:var(--cyan); text-transform:uppercase; font-size:.72rem; font-weight:800; letter-spacing:.17em; margin-bottom:15px; }
    .hero-title { color:#f5f7ff; font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,4.6vw,3.75rem); line-height:1.07; font-weight:700; letter-spacing:-.065em; max-width:880px; }
    .hero-title span { background:linear-gradient(95deg,var(--cyan),#a9bcff 65%,var(--violet)); -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero-description { color:#aab8cf; font-size:1rem; line-height:1.8; max-width:760px; margin-top:16px; margin-bottom:22px; }
    .hero-tags { display:flex; flex-wrap:wrap; gap:9px; }
    .hero-tag { display:inline-block; padding:7px 11px; border-radius:9px; border:1px solid var(--border); background:rgba(255,255,255,.035); color:#cad5e9; font-size:.76rem; font-weight:600; }

    .section-kicker { font-size:.71rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color:var(--cyan); margin-bottom:7px; }
    .section-heading { font-family:'Space Grotesk',sans-serif; color:var(--text); font-size:1.5rem; font-weight:700; letter-spacing:-.04em; margin-bottom:5px; }
    .section-description { color:var(--muted); font-size:.89rem; line-height:1.65; margin-bottom:18px; }
    .section-card { border:1px solid var(--border); background:linear-gradient(145deg,rgba(17,27,44,.96),rgba(13,20,35,.96)); border-radius:18px; padding:20px; margin-bottom:14px; }
    .mini-label { color:#8fa2bc; text-transform:uppercase; font-size:.67rem; font-weight:800; letter-spacing:.12em; margin-bottom:10px; }
    .flag-value { color:#f5f7ff; font-family:'DM Mono',monospace; font-size:clamp(1.2rem,2.7vw,2rem); font-weight:500; overflow-wrap:anywhere; letter-spacing:-.04em; }
    .flag-description { color:#9bacc5; font-size:.8rem; margin-top:8px; line-height:1.65; }
    .flag-chip { display:inline-block; font-family:'DM Mono',monospace; font-size:.82rem; background:rgba(86,224,233,.09); border:1px solid rgba(86,224,233,.24); border-radius:7px; color:#9ef8fa; padding:5px 9px; }
    .flag-chip-violet { background:rgba(167,139,250,.1); border-color:rgba(167,139,250,.26); color:#d6c8ff; }
    .trace-panel { border:1px solid var(--border); background:linear-gradient(140deg,rgba(16,24,39,.9),rgba(12,20,34,.9)); border-radius:15px; padding:17px; margin:7px 0 14px; }
    .trace-label { color:#8fa2bc; font-size:.68rem; text-transform:uppercase; letter-spacing:.11em; font-weight:800; margin-bottom:9px; }
    .output-heading { color:#e8efff; font-family:'Space Grotesk',sans-serif; font-size:1.04rem; font-weight:700; letter-spacing:-.02em; margin-bottom:3px; }
    .output-subtitle { color:#91a3bc; font-size:.81rem; line-height:1.55; margin:4px 0 12px; }
    .step-number { display:inline-flex; justify-content:center; align-items:center; width:27px; height:27px; border-radius:8px; color:var(--cyan); background:rgba(86,224,233,.10); border:1px solid rgba(86,224,233,.22); font-family:'DM Mono',monospace; font-size:.73rem; font-weight:700; margin-right:8px; }
    .pipeline { display:flex; gap:8px; align-items:stretch; margin:20px 0 24px; }
    .pipeline-step { flex:1; min-width:0; padding:13px 10px; border:1px solid var(--border); border-radius:12px; background:rgba(255,255,255,.025); text-align:center; }
    .pipeline-number { color:var(--cyan); font-family:'DM Mono',monospace; font-size:.69rem; margin-bottom:6px; }
    .pipeline-title { color:#e8eef9; font-size:.78rem; font-weight:700; line-height:1.4; }
    .pipeline-arrow { display:flex; align-items:center; color:#637894; }
    .metadata-card { border:1px solid rgba(167,139,250,.24); background:rgba(167,139,250,.055); border-radius:15px; padding:18px; margin:12px 0 17px; }
    .metadata-title { color:#d6c8ff; font-size:.9rem; font-weight:700; margin-bottom:9px; }
    .metadata-line { color:#c0cbe0; font-size:.85rem; line-height:1.85; }
    .success-panel { border:1px solid rgba(87,230,167,.28); background:linear-gradient(135deg,rgba(87,230,167,.08),rgba(16,31,35,.55)); border-radius:17px; padding:21px; margin-top:15px; }
    .success-title { color:#8bf0bb; font-size:.75rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; margin-bottom:9px; }
    .success-message { color:#effff6; font-size:1.15rem; font-weight:700; line-height:1.7; overflow-wrap:anywhere; }
    .footer { color:#71829c; text-align:center; font-size:.77rem; line-height:1.8; border-top:1px solid var(--border); margin-top:44px; padding-top:22px; }

    div[data-testid="stTextArea"] textarea { background:#0c1423 !important; color:#e7f0ff !important; border:1px solid rgba(128,153,190,.26) !important; border-radius:13px !important; font-family:'DM Mono',monospace !important; font-size:.94rem !important; line-height:1.7 !important; }
    div[data-testid="stTextArea"] textarea:focus { border-color:rgba(86,224,233,.8) !important; box-shadow:0 0 0 2px rgba(86,224,233,.08) !important; }
    div[data-testid="stTextArea"] label, div[data-testid="stRadio"] label { color:#dce7fa !important; font-weight:600 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] { gap:10px; }
    div[data-testid="stRadio"] div[role="radiogroup"] label { border:1px solid var(--border); border-radius:11px; padding:9px 13px; background:rgba(255,255,255,.025); }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover { border-color:rgba(86,224,233,.4); background:rgba(86,224,233,.04); }
    div.stButton > button { border-radius:12px; min-height:46px; font-family:'DM Sans',sans-serif; font-weight:700; transition:all .2s ease; }
    div.stButton > button[kind="primary"] { background:linear-gradient(100deg,#44cbd7,#8b88ff); color:#07111d; border:none; box-shadow:0 5px 22px rgba(86,224,233,.10); }
    div.stButton > button[kind="primary"]:hover { filter:brightness(1.08); box-shadow:0 7px 27px rgba(86,224,233,.19); transform:translateY(-1px); }
    div.stButton > button[kind="secondary"] { background:rgba(255,255,255,.035); border:1px solid var(--border); color:#e0eaff; }
    div[data-testid="stMetric"] { border:1px solid var(--border); padding:14px 16px; border-radius:14px; background:rgba(255,255,255,.025); }
    div[data-testid="stMetricLabel"] { color:#94a7c2 !important; }
    div[data-testid="stMetricValue"] { color:#f0f5ff !important; font-family:'Space Grotesk',sans-serif !important; }
    div[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:12px; overflow:hidden; }
    div[data-testid="stExpander"] { background:rgba(255,255,255,.018); border:1px solid var(--border); border-radius:13px; }
    div[data-testid="stAlert"] { border-radius:12px; }
    div[data-testid="stCode"] { border:1px solid rgba(128,153,190,.17); border-radius:11px; }
    hr { border-color:var(--border) !important; }
    @media (max-width:700px) {
        .block-container { padding-left:1rem; padding-right:1rem; padding-top:1rem; }
        .hero { border-radius:19px; }
        .topbar { align-items:flex-start; }
        .top-pill { font-size:.64rem; padding:7px 9px; }
        .pipeline { flex-wrap:wrap; }
        .pipeline-step { flex-basis:38%; }
        .pipeline-arrow { display:none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# UI HELPERS
# ============================================================
def section_header(kicker: str, title: str, description: str) -> None:
    st.markdown(
        f'<div class="section-kicker">{kicker}</div>'
        f'<div class="section-heading">{title}</div>'
        f'<div class="section-description">{description}</div>',
        unsafe_allow_html=True,
    )


def step_header(number: str, title: str, description: str = "") -> None:
    st.markdown(
        f'<div class="output-heading"><span class="step-number">{number}</span>{title}</div>'
        f'<div class="output-subtitle">{description}</div>',
        unsafe_allow_html=True,
    )


def code_panel(label: str, value: str, language: str = "text") -> None:
    st.markdown(f'<div class="trace-label">{label}</div>', unsafe_allow_html=True)
    st.code(str(value) if value else "(empty)", language=language)


def utf8_size(text: str) -> int:
    return len(text.encode("utf-8"))


# ============================================================
# TOP BAR + HERO
# ============================================================
st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <div class="brand-icon">📡</div>
            <div>FrameLab<span class="brand-sub">DATA LINK LAYER LABORATORY</span></div>
        </div>
        <div class="top-pill"><span class="status-dot"></span> SIMULATION ENVIRONMENT</div>
    </div>
    <div class="hero">
        <div class="hero-eyebrow">COMPUTER NETWORKS · CBP PROJECT</div>
        <div class="hero-title">From raw data to<br><span>reliable frames.</span></div>
        <div class="hero-description">
            Explore how the Data Link Layer separates messages into frames.
            Inspect boundary flags, follow every stuffing operation, and verify
            that the receiver reconstructs the original message.
        </div>
        <div class="hero-tags">
            <span class="hero-tag">01 &nbsp; Byte Stuffing Demonstration</span>
            <span class="hero-tag">02 &nbsp; Bit Stuffing</span>
            <span class="hero-tag">03 &nbsp; Frame Boundaries</span>
            <span class="hero-tag">04 &nbsp; Receiver Verification</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONFIGURATION
# ============================================================
section_header(
    "STEP 01 / CONFIGURATION",
    "Choose your framing technique",
    "Select a method and prepare a message for the simulator.",
)

framing = st.radio(
    "FRAMING METHOD",
    ["Byte stuffing", "Bit stuffing"],
    horizontal=True,
    key="framing_mode",
)

if framing == "Byte stuffing":
    st.markdown(
        """
        <div class="section-card">
            <div class="mini-label">ACTIVE CONFIGURATION · CUSTOM RESTORATION MODE</div>
            <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;">
                <div><div class="mini-label">BOUNDARY FLAG</div><div class="flag-value">@</div></div>
                <div style="flex:1;min-width:200px;">
                    <div class="flag-description">The @ character marks the beginning and end of a frame in this educational demonstration.</div>
                    <div style="margin-top:12px;"><span class="flag-chip">@ payload @</span><span style="color:#879ab5;font-size:.77rem;margin-left:9px;">START · PAYLOAD · END</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "This mode follows the requested reversible example: reserved `@` characters "
        "are omitted from the intermediate payload and their positions are transmitted "
        "as metadata. This is a custom educational scheme, not conventional "
        "escape-based byte stuffing."
    )
else:
    st.markdown(
        """
        <div class="section-card">
            <div class="mini-label">ACTIVE CONFIGURATION · BIT STUFFING</div>
            <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;">
                <div><div class="mini-label">HDLC-STYLE FLAG</div><div class="flag-value" style="color:#c9bbff;">01111110</div></div>
                <div style="flex:1;min-width:200px;">
                    <div class="flag-description">The eight-bit pattern marks frame boundaries. A 0 is inserted after five consecutive 1 bits in the payload.</div>
                    <div style="margin-top:12px;"><span class="flag-chip flag-chip-violet">01111110</span><span style="color:#879ab5;font-size:.77rem;margin-left:9px;">START · DATA · END</span></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "Bit stuffing works on binary data. A `0` is inserted after five consecutive "
        "`1` bits in the payload so the flag pattern does not accidentally appear "
        "inside the data."
    )


# ============================================================
# INPUT — FIXED SAMPLE BUTTON CALLBACK
# ============================================================
section_header(
    "STEP 02 / INPUT",
    "Prepare your message",
    "Type a message or load a sample suited to the selected technique.",
)

input_col, workflow_col = st.columns([1.5, 1], gap="large")

with input_col:
    message = st.text_area(
        "MESSAGE PAYLOAD",
        key="message_input",
        height=130,
        max_chars=5000,
        placeholder="Type your message here...",
        help=(
            "Byte mode: try hello@world. Bit mode: try a message such as A~B}C."
        ),
    )
    st.caption(f"UTF-8 size: {utf8_size(message):,} bytes  ·  Characters: {len(message):,}")

    button_col1, button_col2 = st.columns([1.55, 1], gap="small")
    with button_col1:
        run_clicked = st.button(
            "▶  Run transmission",
            type="primary",
            use_container_width=True,
        )
    with button_col2:
        # IMPORTANT: use a callback. Do not assign message_input inside an
        # `if sample_clicked:` block after the text_area widget was created.
        st.button(
            "Load sample",
            on_click=load_sample,
            use_container_width=True,
            help="Load a sample for the currently selected technique.",
        )

with workflow_col:
    st.markdown(
        """
        <div class="section-card" style="height:100%;">
            <div class="mini-label">TRANSMISSION WORKFLOW</div>
            <div style="display:flex;flex-direction:column;gap:11px;">
                <div style="display:flex;gap:12px;align-items:center;"><span class="step-number">01</span><div><b style="color:#eaf1ff;">Input</b><div style="color:#8497b1;font-size:.78rem;">Read the message</div></div></div>
                <div style="height:11px;border-left:1px dashed #40516a;margin-left:13px;"></div>
                <div style="display:flex;gap:12px;align-items:center;"><span class="step-number">02</span><div><b style="color:#eaf1ff;">Encode</b><div style="color:#8497b1;font-size:.78rem;">Apply the selected technique</div></div></div>
                <div style="height:11px;border-left:1px dashed #40516a;margin-left:13px;"></div>
                <div style="display:flex;gap:12px;align-items:center;"><span class="step-number">03</span><div><b style="color:#eaf1ff;">Transmit</b><div style="color:#8497b1;font-size:.78rem;">Build a framed message</div></div></div>
                <div style="height:11px;border-left:1px dashed #40516a;margin-left:13px;"></div>
                <div style="display:flex;gap:12px;align-items:center;"><span class="step-number">04</span><div><b style="color:#eaf1ff;">Decode</b><div style="color:#8497b1;font-size:.78rem;">Recover and verify</div></div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RUN SIMULATION
# ============================================================
if run_clicked:
    st.session_state["simulation_error"] = None
    if not message:
        st.session_state["framing_result"] = None
        st.session_state["simulation_error"] = "Enter a message before running the simulation."
    else:
        try:
            result = simulate(message, framing)
            st.session_state["framing_result"] = result
            st.session_state["last_run_message"] = message
            st.session_state["last_run_framing"] = framing
        except Exception as exc:
            st.session_state["framing_result"] = None
            st.session_state["simulation_error"] = str(exc)

if st.session_state.get("simulation_error"):
    st.error(st.session_state["simulation_error"])


# ============================================================
# TRANSMISSION TRACE
# ============================================================
result = st.session_state.get("framing_result")
if result:
    last_message = st.session_state.get("last_run_message")
    last_framing = st.session_state.get("last_run_framing")

    if last_message != message or last_framing != framing:
        st.info("Your input or technique has changed. Click **Run transmission** to refresh the results.")
    else:
        trace = result["trace"]
        body = str(trace.get("stuffed_body", ""))
        frame = str(trace.get("frame", ""))
        recovered = str(result.get("recovered_message", ""))

        positions = trace.get("restoration_positions", []) if framing == "Byte stuffing" else []
        original_bits = str(trace.get("original_bits", "")) if framing == "Bit stuffing" else ""
        inserted_count = max(0, len(body) - len(original_bits)) if framing == "Bit stuffing" else len(positions)
        payload_length = len(body)
        payload_unit = "bits" if framing == "Bit stuffing" else "characters"

        st.markdown("---")
        section_header(
            "STEP 03 / LIVE TRACE",
            "Transmission breakdown",
            "Follow the message from its original form to the transmitted frame and reconstructed receiver output.",
        )

        metric1, metric2, metric3, metric4 = st.columns(4, gap="medium")
        metric1.metric("Input characters", f"{len(message):,}")
        metric2.metric("Payload length", f"{payload_length:,}", help=f"Measured in {payload_unit}.")
        metric3.metric("Frame length", f"{len(frame):,}")
        metric4.metric("" + ("Inserted bits" if framing == "Bit stuffing" else "Restoration points"), f"{inserted_count:,}")

        st.markdown(
            """
            <div class="pipeline">
                <div class="pipeline-step"><div class="pipeline-number">01 / SOURCE</div><div class="pipeline-title">Original message</div></div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step"><div class="pipeline-number">02 / ENCODE</div><div class="pipeline-title">Stuffing stage</div></div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step"><div class="pipeline-number">03 / FRAME</div><div class="pipeline-title">Boundary flags</div></div>
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step"><div class="pipeline-number">04 / DECODE</div><div class="pipeline-title">Recovered message</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if framing == "Byte stuffing":
            left, right = st.columns(2, gap="large")
            with left:
                step_header("01", "Original message", "The source text before the framing transformation.")
                code_panel("SOURCE TEXT", result["message"])

                step_header("02", "Character inspection", "Inspect how each character is handled.")
                steps = trace.get("steps", [])
                if steps:
                    st.dataframe(pd.DataFrame(steps), use_container_width=True, hide_index=True)
                else:
                    st.caption("No character-level operations were returned.")

            with right:
                step_header("03", "Intermediate payload", "Reserved @ characters are omitted from the payload.")
                code_panel("READABLE PAYLOAD", body)

                step_header("04", "Complete transmitted frame", "The payload is surrounded by boundary flags.")
                code_panel("START FLAG + PAYLOAD + END FLAG", frame)
                st.markdown(
                    '<span class="flag-chip">START FLAG: @</span> '
                    '<span class="flag-chip">END FLAG: @</span>',
                    unsafe_allow_html=True,
                )

            restoration_char = trace.get("restoration_character", "@")
            positions_display = positions if positions else "None"
            st.markdown(
                f"""
                <div class="metadata-card">
                    <div class="metadata-title">✦ Restoration metadata</div>
                    <div class="metadata-line">Character to restore: <span class="flag-chip flag-chip-violet">{restoration_char}</span></div>
                    <div class="metadata-line">Original zero-based positions: <span class="flag-chip flag-chip-violet">{positions_display}</span></div>
                    <div class="metadata-line" style="margin-top:8px;color:#aebbd0;">This metadata tells the receiver where omitted characters belonged. The payload alone cannot uniquely reconstruct the original message.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            left, right = st.columns(2, gap="large")
            with left:
                step_header("01", "Original message", "The readable input supplied by the user.")
                code_panel("SOURCE TEXT", result["message"])

                step_header("02", "Binary conversion", "UTF-8 bytes represented as eight-bit groups.")
                code_panel("ORIGINAL DATA BITS", original_bits)
                st.caption(f"Original data contains {len(original_bits):,} bits.")

            with right:
                step_header("03", "Stuffing operations", "A zero is inserted after five consecutive one bits.")
                steps = trace.get("steps", [])
                if steps:
                    st.dataframe(pd.DataFrame(steps), use_container_width=True, hide_index=True)
                else:
                    st.info("No stuffing operations were recorded for this input.")

                step_header("04", "Stuffed payload", "The intermediate binary sequence after stuffing.")
                code_panel("STUFFED DATA BITS", body)

            step_header("05", "Complete transmitted frame", "Boundary flags surround the stuffed payload.")
            code_panel("TRANSMITTED FRAME", frame)
            flag_a, flag_b, flag_c = st.columns([1, 1.4, 1])
            with flag_a:
                st.markdown('<div class="section-card"><div class="mini-label">START FLAG</div><div class="flag-value" style="font-size:1.2rem;">01111110</div></div>', unsafe_allow_html=True)
            with flag_b:
                st.markdown('<div class="section-card"><div class="mini-label">STUFFED DATA</div><div style="font-family:DM Mono,monospace;color:#c9bbff;">Payload bits</div></div>', unsafe_allow_html=True)
            with flag_c:
                st.markdown('<div class="section-card"><div class="mini-label">END FLAG</div><div class="flag-value" style="font-size:1.2rem;">01111110</div></div>', unsafe_allow_html=True)
            st.caption(f"Stuffed payload contains {len(body):,} bits, including {inserted_count:,} additional zero bit(s).")

        # Receiver result
        st.markdown("---")
        section_header(
            "STEP 04 / DESTINATION",
            "Receiver reconstruction",
            "The receiver reverses the transformation and checks the recovered output.",
        )
        if recovered == message:
            st.markdown(
                f"""
                <div class="success-panel">
                    <div class="success-title">✓ ROUND-TRIP VERIFICATION PASSED</div>
                    <div class="success-message">{len(recovered):,} characters successfully recovered</div>
                    <div style="color:#a5cdb8;font-size:.83rem;margin-top:8px;">The recovered message matches the original input.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown('<div class="trace-label" style="margin-top:17px;">RECOVERED MESSAGE</div>', unsafe_allow_html=True)
            st.code(recovered if recovered else "(empty)", language="text")
        else:
            st.error("Round-trip verification failed. The recovered message differs from the original input.")
            st.markdown("**Original message**")
            st.code(message if message else "(empty)", language="text")
            st.markdown("**Recovered message**")
            st.code(recovered if recovered else "(empty)", language="text")

        with st.expander("Advanced inspection · hexadecimal byte values"):
            st.markdown("Hexadecimal is useful for inspecting raw byte values, but it is optional for understanding the main demonstration.")
            original_bytes = result.get("original_bytes", "")
            st.code(str(original_bytes) if original_bytes else "(no bytes)", language="text")


# ============================================================
# QUICK REFERENCE
# ============================================================
st.markdown("---")
section_header(
    "REFERENCE / QUICK GUIDE",
    "Understand the two techniques",
    "Both methods help mark frame boundaries, but they operate on different representations.",
)

guide_left, guide_right = st.columns(2, gap="large")
with guide_left:
    st.markdown(
        """
        <div class="section-card" style="height:100%;">
            <div style="font-size:1.5rem;margin-bottom:10px;">🔤</div>
            <div class="output-heading">Byte / special-character demonstration</div>
            <div class="output-subtitle">The custom mode removes reserved @ characters from the intermediate payload and restores them using position metadata.</div>
            <div class="mini-label">EXAMPLE</div>
            <div style="font-family:'DM Mono',monospace;color:#eef4ff;line-height:2;">Original: hello@world<br>Payload: helloworld<br>Receiver: hello@world</div>
            <div class="flag-description">Position metadata is essential. Conventional byte stuffing typically escapes reserved bytes instead of deleting them.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with guide_right:
    st.markdown(
        """
        <div class="section-card" style="height:100%;">
            <div style="font-size:1.5rem;margin-bottom:10px;">0️⃣</div>
            <div class="output-heading">Bit stuffing</div>
            <div class="output-subtitle">A zero is inserted after five consecutive one bits; the receiver removes the inserted zeros.</div>
            <div class="mini-label">STANDARD FLAG PATTERN</div>
            <div class="flag-value" style="font-size:1.45rem;color:#c9bbff;">01111110</div>
            <div class="flag-description">Stuffing prevents the flag pattern from appearing unintentionally inside the payload.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        <div style="color:#aabbd3;font-weight:700;margin-bottom:5px;">FRAMELAB · DATA LINK LAYER SIMULATOR</div>
        Computer Networks CBP · Educational software simulation<br>
        Demonstrates framing and reversible reconstruction. No live network transmission or CRC implementation.
    </div>
    """,
    unsafe_allow_html=True,
)
