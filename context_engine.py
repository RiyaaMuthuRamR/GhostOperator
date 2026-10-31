import os
from pathlib import Path

IGNORED_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", ".idea", ".vscode"}

def get_directory_context(root_dir=None):
    root = Path(root_dir or Path.cwd()).resolve()
    context_files = []
    
    for current, dirs, filenames in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for filename in filenames:
            path = Path(current) / filename
            try:
                relative = path.relative_to(root)
                stat = path.stat()
                context_files.append({
                    "name": str(relative),
                    "size_bytes": stat.st_size,
                    "extension": path.suffix.lower(),
                    "last_modified": int(stat.st_mtime)
                })
            except (OSError, ValueError):
                continue
                
    return {"workspace_root": str(root), "files": context_files}
