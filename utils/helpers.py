from pathlib import Path

def create_folders():
    folders = [
        "videos",
        "clips",
        "output",
        "json",
        "csv",
        "pdf",
        "models",
        "temp"
    ]

    for folder in folders:
        Path(folder).mkdir(exist_ok=True)

    print("Folders created successfully!")