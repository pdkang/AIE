from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Import our local utilities instead of aimakerspace
from text_utils import CharacterTextSplitter, TextFileLoader, PDFLoader
from openai_utils import SystemRolePrompt, UserRolePrompt, ChatOpenAI
from vector_store import VectorDatabase

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prompt templates
system_template = """\
Use the following context to answer a users question. If you cannot find the answer in the context, say you don't know the answer."""
system_role_prompt = SystemRolePrompt(system_template)

user_prompt_template = """\
Context:
{context}

Question:
{question}
"""
user_role_prompt = UserRolePrompt(user_prompt_template)

# Initialize components
text_splitter = CharacterTextSplitter()
chat_openai = ChatOpenAI()

# Store vector databases for each session
vector_dbs = {}

class QueryRequest(BaseModel):
    session_id: str
    query: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save file temporarily
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Process file
        loader = PDFLoader(file_path) if file.filename.lower().endswith('.pdf') else TextFileLoader(file_path)
        documents = loader.load_documents()
        texts = text_splitter.split_texts(documents)

        # Create vector database
        vector_db = VectorDatabase()
        vector_db = await vector_db.abuild_from_list(texts)

        # Generate session ID and store vector_db
        import uuid
        session_id = str(uuid.uuid4())
        vector_dbs[session_id] = vector_db

        # Cleanup
        os.remove(file_path)

        return {"session_id": session_id, "message": "File processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query(request: QueryRequest):
    try:
        vector_db = vector_dbs.get(request.session_id)
        if not vector_db:
            raise HTTPException(status_code=404, detail="Session not found")

        # Retrieve context
        context_list = await vector_db.search_by_text(request.query, k=4)
        context_prompt = "\n".join([str(context[0]) for context in context_list])

        # Generate prompts
        formatted_system_prompt = system_role_prompt.create_message()
        formatted_user_prompt = user_role_prompt.create_message(
            question=request.query, 
            context=context_prompt
        )

        # Get response
        response = await chat_openai.acomplete(
            [formatted_system_prompt, formatted_user_prompt]
        )

        return {
            "answer": str(response),
            "context": [str(context[0]) for context in context_list]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Cleanup endpoint
@app.delete("/session/{session_id}")
async def cleanup_session(session_id: str):
    if session_id in vector_dbs:
        del vector_dbs[session_id]
        return {"message": "Session cleaned up successfully"}
    raise HTTPException(status_code=404, detail="Session not found")

# Serve static files from static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html') 