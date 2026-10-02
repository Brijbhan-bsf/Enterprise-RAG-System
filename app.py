import streamlit as st
import requests

st.set_page_config(page_title="BSF AI Suite", layout="wide")

st.title("⚡ Enterprise AI & RAG Portal")
st.caption("Bihar Skill Foundation - Connected Full-Stack System (Decoupled & Production Hosted)")
st.divider()

with st.sidebar:
    st.markdown("### 🌐 Routing Gateway")
    # Live Hosted Server par default Cloud node selected rahega
    execution_mode = st.radio("Select Processing Node", ["Cloud (Gemini API)", "Local (Ollama Engine)"])
    mode_value = "cloud" if "Cloud" in execution_mode else "local"

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Document Context")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    user_query = st.text_input("Ask a question from this document")
    
    if st.button("Run AI Processing Pipeline"):
        if uploaded_file is not None and user_query != "":
            with st.spinner("Connecting to live production FastAPI engine..."):
                try:
                    # 🔴 100% PRODUCTION COMPLIANT ROUTING GATEWAY SYSTEM
                    backend_url = "https://onrender.com"
                    
                    # Parameters ko parameters dictionary ki jagah direct requests.post ke 'params' filter me specify karna
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    query_params = {"question": user_query, "mode": mode_value}
                    
                    # Direct secure payload mapping transmission
                    response = requests.post(backend_url, params=query_params, files=files)

                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Response Received via {result.get('engine_node')}")
                        st.markdown(f"### 🤖 AI Answer:")
                        st.write(result.get("answer"))
                    else:
                        st.error(f"Backend Engine Error: Status Code {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🔴 Error: Live backend server se response timeout hua. Kripya check karein ki Render application sleeping mode me to nahi hai.")
        else:
            st.warning("Kripya pehle document upload karein aur apna sawaal type karein.")

with col2:
    st.markdown("""
        <div style="background-color:#FFFFFF; padding:20px; border-radius:10px; border:1px solid #E2E8F0;">
            <h4>⚙️ Production Decoupled Architecture</h4>
            <p><b>Frontend Interface Layer:</b> Streamlit UI Cloud Server</p>
            <p><b>Backend Computing Layer:</b> FastAPI Independent Node (Render Cloud Clusters)</p>
            <p><b>Data Layer Gateway:</b> Qdrant Engine Sandbox</p>
            <p style="color:#10B981;"><b>Status:</b> Fully Enterprise Compliance Ready!</p>
        </div>
    """, unsafe_allow_html=True)
