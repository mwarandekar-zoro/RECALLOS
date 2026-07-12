from Backend.database import get_connection


def search_files(query):
    connection = get_connection()

    search_pattern = f"%{query}%"

    rows = connection.execute("""
        SELECT
            id,
            name,
            path,
            extension,
            size,
            content,
            modified_at
        FROM files
        WHERE name LIKE ?
           OR content LIKE ?
        ORDER BY modified_at DESC
    """, (
        search_pattern,
        search_pattern
    )).fetchall()

    connection.close()

    results = []

    for row in rows:
        content = row["content"] or ""

        results.append({
            "id": row["id"],
            "name": row["name"],
            "path": row["path"],
            "extension": row["extension"],
            "size": row["size"],
            "snippet": create_snippet(content, query),
            "modified_at": row["modified_at"]
        })

    return results


def create_snippet(content, query, length=200):
    if not content:
        return ""

    position = content.lower().find(query.lower())

    if position == -1:
        return content[:length]

    start = max(0, position - 60)
    end = min(len(content), position + len(query) + 140)

    snippet = content[start:end].replace("\n", " ")

    if start > 0:
        snippet = "..." + snippet

    if end < len(content):
        snippet += "..."

    return snippet