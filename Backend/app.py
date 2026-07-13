from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from Backend.scanner import scan_folder
from Backend.extractor import extract_text
from Backend.database import create_database, save_file
from Backend.search import search_files


app = FastAPI(
    title="RecallOS API",
    description="Local search engine for your digital life",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
TEST_FILES_DIR = BASE_DIR / "test_files"

# Serve frontend static files from the `frontend` directory
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.on_event("startup")
def startup():
    create_database()


@app.get("/")
def home():
    return {
        "project": "RecallOS",
        "message": "Your digital life search engine is running!",
        "version": "0.1.0"
    }


@app.get("/scan")
def scan():
    files = scan_folder(TEST_FILES_DIR)

    return {
        "total_files": len(files),
        "files": files
    }


@app.post("/index")
def index_files():
    files = scan_folder(TEST_FILES_DIR)

    indexed = []

    for file_info in files:
        content = extract_text(file_info["path"])

        save_file(file_info, content)

        indexed.append({
            "name": file_info["name"],
            "characters_extracted": len(content)
        })

    return {
        "message": "Indexing completed",
        "total_indexed": len(indexed),
        "files": indexed
    }


@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    results = search_files(q)

    return {
        "query": q,
        "total_results": len(results),
        "results": results
    }


@app.get("/ui")
def serve_ui():
    """Serve the RecallOS UI"""
    ui_file = FRONTEND_DIR / "index.html"
    if ui_file.exists():
        return FileResponse(ui_file, media_type="text/html")
    return {"error": "UI file not found"}
