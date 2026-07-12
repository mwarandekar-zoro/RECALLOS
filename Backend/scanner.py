from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}


def scan_folder(folder_path):
    """
    Scan a folder and its subfolders for supported files.
    This function only reads file information.
    It does not delete, edit, move, or rename any files.
    """

    folder = Path(folder_path)

    if not folder.exists():
        return []

    found_files = []

    for file_path in folder.rglob("*"):

        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:

            file_info = {
                "name": file_path.name,
                "path": str(file_path.resolve()),
                "extension": file_path.suffix.lower(),
                "size": file_path.stat().st_size,
                "modified_at": file_path.stat().st_mtime
}

            found_files.append(file_info)

    return found_files