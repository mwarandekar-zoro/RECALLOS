import argparse
from pathlib import Path

from Backend.scanner import scan_folder
from Backend.extractor import extract_text
from Backend.database import create_database, save_file
from Backend.search import search_files


def index_folder(folder_path: Path) -> int:
    create_database()

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    files = scan_folder(folder_path)
    indexed_count = 0

    for file_info in files:
        content = extract_text(file_info["path"])
        save_file(file_info, content)
        indexed_count += 1

    print(f"Indexed {indexed_count} file{'s' if indexed_count != 1 else ''} from {folder_path}")
    return indexed_count


def search_query(query: str, limit: int = 20):
    results = search_files(query)
    print(f"Found {len(results)} result{'s' if len(results) != 1 else ''} for '{query}'\n")

    for result in results[:limit]:
        print(f"- {result['name']} ({result['extension']}, {round(result['size'] / 1024)} KB)")
        print(f"  {result['path']}")
        print(f"  {result['snippet']}\n")

    return results


def main():
    parser = argparse.ArgumentParser(description="RecallOS command-line tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Scan and index files")
    index_parser.add_argument(
        "--folder",
        default="test_files",
        help="Folder to scan for supported files",
    )

    search_parser = subparsers.add_parser("search", help="Search indexed files")
    search_parser.add_argument("--query", "-q", required=True, help="Text query to search")
    search_parser.add_argument("--limit", "-n", type=int, default=20, help="Maximum results to display")

    args = parser.parse_args()

    if args.command == "index":
        index_folder(Path(args.folder))
    elif args.command == "search":
        search_query(args.query, limit=args.limit)


if __name__ == "__main__":
    main()
