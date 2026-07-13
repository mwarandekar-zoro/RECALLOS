# 🧠 RecallOS - Your Personal Memory Search Engine

RecallOS is a **local search engine for your digital life**. Index PDFs, Word docs, images, notes, and more—then search across everything in seconds.

## ✨ Features

- 🔍 **Instant Full-Text Search** — Search across PDFs, Word docs, TXT, Markdown, and images
- 🎨 **Modern Dark UI** — Glass-morphism design with smooth animations
- 📁 **File Type Filters** — Quick filters for PDFs, Word docs, Images, Code, and more
- 📌 **Recent Searches** — Sidebar tracks your last searches for quick re-access
- ⚡ **Fast Indexing** — Extract and index content from multiple file types
- 🖥️ **Local-Only** — Your data never leaves your computer
- 📱 **Responsive** — Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone and setup:**
```bash
cd RecallOS
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

2. **Index your files:**
```bash
python -c "from Backend.scanner import scan_folder; from Backend.extractor import extract_text; from Backend.database import create_database, save_file; from pathlib import Path; create_database(); files = scan_folder(Path('test_files')); [save_file(f, extract_text(f['path'])) for f in files]; print(f'Indexed {len(files)} files')"
```

3. **Start the server:**
```bash
python -m uvicorn Backend.app:app --reload --host 0.0.0.0
```

4. **Open the UI:**
Visit `http://localhost:8000/ui` in your browser
## 🧩 Python CLI Usage

RecallOS now includes a small command-line interface in `Backend/cli.py`.

### Index a folder:
```bash
python -m Backend.cli index --folder test_files
```

### Search indexed content:
```bash
python -m Backend.cli search --query "memory"
```

> Tip: Run `python -m Backend.cli --help` for available commands.
## 📖 Usage

### Search
- Type keywords in the search bar
- Results appear in real-time as you type
- Click result cards to view details

### Filter
- **All** — Show all results
- **📄 PDFs** — PDF documents only
- **📝 Word** — Microsoft Word documents
- **🖼️ Images** — Image files
- **💻 Code** — Code files (Python, JavaScript, etc.)

### Recent Searches
- Click items in the left sidebar to re-search
- Sidebar auto-updates with your latest queries

## 📁 Project Structure

```
RecallOS/
├── index.html              # Frontend UI (React-free SPA)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── Backend/
│   ├── app.py             # FastAPI server
│   ├── scanner.py         # File discovery
│   ├── extractor.py       # Text extraction from files
│   ├── database.py        # SQLite database management
│   └── search.py          # Full-text search
├── data/
│   └── recallos.db        # SQLite database (auto-created)
└── test_files/            # Sample files for testing
```

## 🔧 API Endpoints

### `GET /`
Health check and version info

### `GET /scan`
List all files in test_files directory
```bash
curl http://localhost:8000/scan
```

### `POST /index`
Index all files and extract their content
```bash
curl -X POST http://localhost:8000/index
```

### `GET /search?q=<query>`
Search indexed files by keyword
```bash
curl "http://localhost:8000/search?q=Stack"
```

### `GET /ui`
Serve the frontend UI
```bash
Open http://localhost:8000/ui in browser
```

## 📦 Dependencies

- **FastAPI** — Modern async web framework
- **Uvicorn** — ASGI server
- **PyMuPDF (fitz)** — PDF text extraction
- **python-docx** — Word document parsing
- **Pydantic** — Data validation

## 💾 Database

RecallOS uses **SQLite** (stored in `data/recallos.db`) with a single `files` table:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | File name |
| path | TEXT | File path |
| extension | TEXT | File extension |
| size | INTEGER | File size in bytes |
| content | TEXT | Extracted text content |
| modified_at | TIMESTAMP | Last modified date |

## 🎨 UI Theme

- **Background**: Dark gradient (0a0a0a → 1a1a2e)
- **Accent**: Purple (#8b5cf6) and Indigo (#6366f1)
- **Text**: Light gray (#e0e0e0)
- **Effects**: Glass-morphism, smooth animations

## 🔐 Privacy & Security

- ✅ All processing is local—no cloud uploads
- ✅ Search history stored only in browser (localStorage)
- ✅ No external API calls
- ✅ SQLite database is just a file

## 📝 Supported File Types

- **Documents**: PDF (.pdf), Word (.docx), Text (.txt), Markdown (.md)
- **Images**: JPG (.jpg), PNG (.png), GIF (.gif)
- **Code**: Python (.py), JavaScript (.js), Java (.java), C++ (.cpp)
- **Easily extensible** — Add more types in `Backend/extractor.py`

## 🐛 Troubleshooting

### Python not found
```bash
# Windows: Use the full path
C:\Users\YourName\AppData\Local\Microsoft\WindowsApps\python.exe --version

# Or disable the Windows Store alias:
# Settings > Apps > Advanced app settings > App execution aliases
```

### venv activation fails
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# If it fails, enable script execution:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Server won't start
- Make sure port 8000 is not in use
- Check that all dependencies are installed: `pip install -r requirements.txt`

## 🚀 Deployment

### Local Network Access
To access from other computers on your network:
```bash
python -m uvicorn Backend.app:app --host 0.0.0.0 --port 8000
```
Then visit: `http://<your-ip>:8000/ui`

### Production Deployment
- Use a WSGI server like Gunicorn
- Add authentication (JWT, OAuth)
- Use a production database (PostgreSQL)
- Add rate limiting and CORS restrictions

## 🛣️ Roadmap

- [ ] Add authentication & user accounts
- [ ] Cloud sync (optional)
- [ ] Advanced filtering (date range, file size)
- [ ] Dark/Light theme toggle
- [ ] Web UI improvements (infinite scroll, preview)
- [ ] OCR for scanned PDFs
- [ ] Audio/video metadata extraction
- [ ] Docker containerization

## 🐳 Docker

You can run RecallOS in a container for a reproducible environment.

Build the image:
```bash
docker build -t recallos:latest .
```

Run the container (mount `data/` so the SQLite DB persists):

```bash
# Linux / macOS
docker run --rm -p 8000:8000 -v $(pwd)/data:/home/appuser/app/data recallos:latest

# Windows PowerShell
docker run --rm -p 8000:8000 -v ${PWD}\\data:/home/appuser/app/data recallos:latest
```

Open the UI at `http://localhost:8000/ui`.

Optional `docker-compose.yml` (recommended for local development): create a `docker-compose.yml` with the following content and run `docker compose up --build`:

```yaml
version: '3.8'
services:
	recallos:
		build: .
		ports:
			- "8000:8000"
		volumes:
			- ./data:/home/appuser/app/data
		restart: unless-stopped
```


## 📧 Contributing

Feel free to fork, modify, and improve RecallOS!

## 📄 License

MIT License — Use freely for personal and commercial projects

---

**Made with ⚡ for your digital memory** | [GitHub](https://github.com/mwarandekar-zoro/RECALLOS)
