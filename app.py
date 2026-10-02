import streamlit as st
import requests

st.set_page_config(page_title="BSF AI Suite", layout="wide")

st.title("⚡ Enterprise AI & RAG Portal")
st.caption("Bihar Skill Foundation - Connected Full-Stack System (Decoupled)")
st.divider()

with st.sidebar:
    st.markdown("### 🌐 Routing Gateway")
    execution_mode = st.radio("Select Processing Node", ["Cloud (Gemini API)", "Local (Ollama Engine)"])
    mode_value = "cloud" if "Cloud" in execution_mode else "local"

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Document Context")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    user_query = st.text_input("Ask a question from this document")
    
    if st.button("Run AI Processing Pipeline"):
        if uploaded_file is not None and user_query != "":
            with st.spinner("Connecting to FastAPI backend router..."):
                try:
                    backend_url = "http://localhost:8000/ask-hybrid-rag/"
                    
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    params = {"question": user_query, "mode": mode_value}
                    
                    response = requests.post(backend_url, params=params, files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Response Received via {result.get('engine_node')}")
                        st.markdown(f"### 🤖 AI Answer:")
                        st.write(result.get("answer"))
                    else:
                        st.error(f"Backend Engine Error: Status Code {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🔴 Error: FastAPI backend server nahi chal raha hai! Pehle main.py ko run karein.")
        else:
            st.warning("Kripya pehle document upload karein aur apna sawaal type karein.")

with col2:
    st.markdown("""
        <div style="background-color:#FFFFFF; padding:20px; border-radius:10px; border:1px solid #E2E8F0;">
            <h4>⚙️ Full-Stack Decoupled Info</h4>
            <p><b>Frontend:</b> Streamlit (Port 8501)</p>
            <p><b>Backend:</b> FastAPI (Port 8000)</p>
            <p><b>Future Proof:</b> Decoupled Architecture Ready.</p>
        </div>
    """, unsafe_allow_html=True)
