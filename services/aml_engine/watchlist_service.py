import csv
from pathlib import Path
from typing import List

WATCHLIST_PATH = Path(__file__).resolve().parent / "watchlist.csv"


def load_watchlist(path: Path = WATCHLIST_PATH) -> List[str]:
    names: List[str] = []
    if not path.exists():
        return names

    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("name"):
                names.append(row["name"].strip())
    return names


def match_against_watchlist(name: str, watchlist: List[str] | None = None) -> bool:
    names = watchlist or load_watchlist()
    normalized_name = name.strip().lower()
    for item in names:
        if normalized_name == item.strip().lower():
            return True
    return False
