from pathlib import Path

from fastapi import FastAPI, Query

from Backend.scanner import scan_folder
from Backend.extractor import extract_text
from Backend.database import create_database, save_file
from Backend.search import search_files


app = FastAPI(
    title="RecallOS API",
    description="Local search engine for your digital life",
    version="0.1.0"
)


BASE_DIR = Path(__file__).resolve().parent.parent
TEST_FILES_DIR = BASE_DIR / "test_files"


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
    