from fastapi import FastAPI, UploadFile, File
import pdfplumber
import io
import os
import ollama
from google import genai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Environment aur Key Verification Setup
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

app = FastAPI()

# 2. Universal Local Memory Cluster Config
qdrant_client = QdrantClient(":memory:")
COLLECTION_NAME = "enterprise_docs"

# Nomic vector outputs ke liye size=768 dimensions apply karna
try:
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
except Exception:
    pass

def split_text_into_chunks(text: str, chunk_size: int = 150, chunk_overlap: int = 30):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i : i + chunk_size]
        chunks.append(" ".join(chunk_words))
        i += (chunk_size - chunk_overlap)
    return chunks

# 3. Vectorization Pipeline Interface
def get_real_embedding(text: str):
    try:
        response = ollama.embeddings(model="nomic-embed-text", prompt=text)
        return response["embedding"]
    except Exception:
        # Fallback safety matrix logic inside pipeline
        val = len(text) % 10 / 10.0
        return [val, val*0.2, val*0.5] + [0.1] * 765

@app.get("/")
def home():
    return {"status": "Active", "database": "Qdrant Node Connected"}

# 🔴 UNIVERSAL PRODUCTION ROUTE ENTRYPOINT
@app.post("/ask-hybrid-rag")
async def ask_rag(question: str, file: UploadFile = File(...), mode: str = "cloud"):
    file_content = await file.read()
    # ... baki code poora same rahega ...
    pdf_stream = io.BytesIO(file_content)
    extracted_text = ""
    
    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
                
    chunks = split_text_into_chunks(extracted_text)
    
    # Points registration setup
    points = []
    for idx, chunk in enumerate(chunks):
        vector = get_real_embedding(chunk)
        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={"text": chunk, "source": file.filename}
            )
        )
    
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    # 🔴 FIXED SEARCH ROUTE: Latest SDK using .query_points()
    query_vector = get_real_embedding(question)
    search_result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,       # Changed from query_vector to query parameter
        limit=2
    )
    
    # Matched vectors mapping context directly out of Points array structure
    matched_contexts = [hit.payload["text"] for hit in search_result.points]
    context = " ".join(matched_contexts) if matched_contexts else "No context fetched"
    
    prompt = f"Context from Qdrant DB: {context}\n\nQuestion: {question}\n\nAnswer based strictly on context in short Hindi/Hinglish."

    # Hybrid Node Router Selection Execution
    if mode == "local":
        try:
            response = ollama.generate(model='llama3:latest', prompt=prompt)
            ai_response = response['response']
            engine_used = "Ollama Local Node (Llama 3) + Qdrant DB"
        except Exception:
            try:
                client = genai.Client(api_key=GEMINI_KEY)
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
                ai_response = f"{response.text}\n\n*(Note: Local model fallback triggered)*"
                engine_used = "Gemini 3.8 (Local Fallback Mode) + Qdrant DB"
            except Exception as e:
                ai_response = f"Cluster connection missing inside local framework: {str(e)}"
                engine_used = "Hybrid Node Offline"
    else:
        try:
            client = genai.Client(api_key=GEMINI_KEY)
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            ai_response = response.text
            engine_used = "Google Gemini 3.8 + Qdrant Vector Cluster"
        except Exception:
            try:
                client = genai.Client(api_key=GEMINI_KEY)
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                )
                ai_response = response.text
                engine_used = "Google Gemini 3.5 Cloud (Backup Node)"
            except Exception as e_cloud:
                ai_response = f"Cloud gateway error code detected: {str(e_cloud)}"
                engine_used = "Gemini Cloud Cluster (Failed)"

    return {
        "status": "Success",
        "engine_node": engine_used,
        "answer": ai_response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
