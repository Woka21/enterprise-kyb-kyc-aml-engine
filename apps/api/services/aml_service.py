import csv
from pathlib import Path
from typing import Dict, Any, List
from difflib import SequenceMatcher

WATCHLIST_PATH = Path(__file__).resolve().parent.parent / "data" / "watchlist.csv"


def load_sanctions_watchlist() -> List[Dict[str, str]]:
    """
    Load the local sanctions and PEP watchlist from CSV.
    In production, this would be synced with OpenSanctions daily.
    """
    watchlist = []
    if not WATCHLIST_PATH.exists():
        return watchlist

    try:
        with WATCHLIST_PATH.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                watchlist.append(row)
    except Exception as e:
        print(f"Error loading watchlist: {e}")
    return watchlist


def fuzzy_match(name: str, watchlist_entries: List[Dict[str, str]], threshold: float = 0.85) -> bool:
    """
    Use fuzzy matching to detect possible matches in the watchlist.
    """
    normalized_name = name.strip().lower()
    for entry in watchlist_entries:
        watchlist_name = entry.get("name", "").strip().lower()
        similarity = SequenceMatcher(None, normalized_name, watchlist_name).ratio()
        if similarity >= threshold:
            return True
    return False


def check_aml_watchlist(director_name: str) -> Dict[str, Any]:
    """
    Check director name against local sanctions and PEP watchlist.
    Returns match status and details if found.
    """
    try:
        watchlist = load_sanctions_watchlist()
        is_match = fuzzy_match(director_name, watchlist)

        if is_match:
            # Find the matching entry
            for entry in watchlist:
                if fuzzy_match(director_name, [entry]):
                    return {
                        "match": True,
                        "name": director_name,
                        "watchlist_entry": entry.get("name"),
                        "category": entry.get("category"),
                        "source": entry.get("source"),
                        "status": "FLAGGED",
                    }
        else:
            return {
                "match": False,
                "name": director_name,
                "status": "CLEAR",
                "message": "No sanctions or PEP match found",
            }
    except Exception as e:
        return {"match": False, "error": str(e)}
