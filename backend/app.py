from fastapi import FastAPI, UploadFile
import shutil
from process import process_pdf
from rag import answer_query

app = FastAPI()

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    file_location = f"data/uploads/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    num_chunks = process_pdf(file_location)
    return {"message": "PDF processed", "chunks": num_chunks}


@app.get("/ask")
async def ask_question(q: str):
    answer = answer_query(q)
    return {"answer": answer}
