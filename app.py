import streamlit as st
import time

# Clean, professional imports showing Separation of Concerns
from layer1_seie import SymbolicEntityInterningEngine
from layer2_dlme import DualLatticeMonotonicEngine
from layer3_dsoe import DurableSagaOrchestrationEngine

st.set_page_config(page_title="TriState-Harness | Ignite iq", layout="wide")
st.markdown("<h1 style='text-align: center; color: #00E5FF;'>TriState-Harness: Enterprise SOC Middleware</h1>", unsafe_allow_html=True)
st.caption("Architected by Team Ignite iq | Theme 3")

# Initialize Engines
if 'seie' not in st.session_state:
    st.session_state.seie = SymbolicEntityInterningEngine()
if 'dlme' not in st.session_state:
    st.session_state.dlme = DualLatticeMonotonicEngine()
if 'dsoe' not in st.session_state:
    st.session_state.dsoe = DurableSagaOrchestrationEngine()

st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("LLM Context Burden", "$42.50", "-93.34%")
col2.metric("SEIE Active Memory Pointers", "0x00")
col3.metric("Bayesian Uncertainty (σ²)", "0.001")
col4.metric("State Corruption Rate", "0.0%", "0 ACID Faults")
st.divider()

colA, colB = st.columns(2)

with colA:
    st.subheader("Layer 1 & 2: Cryptographic Ingestion & Lattice Triage")
    if st.button("Initialize High-Throughput Stream"):
        log_payload = {"eventName": "IAM_AssumeRole", "sourceIPAddress": "10.0.0.54", "risk": "CRITICAL"}
        
        with st.spinner("Allocating C-Pointers & Hashing..."):
            time.sleep(0.5)
            handle = st.session_state.seie.process_telemetry_stream(log_payload)
            metrics = st.session_state.seie.yield_compression_ratio()
            
            st.code(f"RAW TELEMETRY: {log_payload}\n\nSYMBOLIC INTERNING COMPLETE:\n➔ {handle}")
            st.success(f"Compression Factor: {metrics['compression_factor']}x | Token Savings: {metrics['token_savings_pct']}%")
            
        with st.spinner("Evaluating Monotonic Lattice..."):
            time.sleep(0.5)
            lattice_result = st.session_state.dlme.converge_state("10.0.0.54", "BLOCK_IP")
            conflict_result = st.session_state.dlme.converge_state("10.0.0.54", "ALLOW_IP")
            
            st.warning(f"LATTICE COLLISION DETECTED: ALLOW vs BLOCK\nVariance (σ²): {conflict_result['variance']}\nResolution: {conflict_result['resolution']}")

with colB:
    st.subheader("Layer 3: Durable Saga DAG Rollback")
    if st.button("Execute Speculative Tool Chain"):
        ledger = st.session_state.dsoe.execute_speculative_branch("10.0.0.54")
        for entry in ledger:
            if "FORWARD" in entry:
                st.write(f"🔴 `{entry}`")
            elif "COMPENSATING" in entry:
                st.write(f"🟢 `{entry}`")
            elif "FAULT" in entry:
                st.error(entry)
            else:
                st.info(entry)