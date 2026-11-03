import os
import re

FILLER_WORDS = ["um", "uh", "like", "basically", "actually", "you know",
                "i mean", "sort of", "kind of", "literally", "so yeah"]

STAR_CUES = {
    "situation": ["when i was", "at my previous", "the situation", "we were facing", "in my last role"],
    "task":      ["my responsibility", "i was asked", "my goal", "i needed to", "the task"],
    "action":    ["i decided", "i implemented", "i built", "i led", "so i", "i reached out"],
    "result":    ["as a result", "which led to", "increased", "reduced", "%", "in the end", "outcome"],
}

def detect_filler_words(answer: str) -> dict:
    """flags filler words like "um", "like", "basically" and return complete stats"""
    text = answer.lower()
    counts = {}
    for f in FILLER_WORDS:
        n = len(re.findall(rf"\b{re.escape(f)}\b", text))   # \b = whole word only
        if n:
            counts[f] = n
    total_words = len(text.split())
    total_fillers = sum(counts.values())
    return {
        "filler_count": total_fillers,
        "fillers_found": counts,            # {"um": 3, "like": 2}
        "filler_ratio": round(total_fillers / max(total_words, 1), 3),
        "verdict": "clean" if total_fillers <= 2 else "too many fillers",
    }

def check_star_structure(answer: str) -> dict:
    """checks whether a behavioral answer covers Situation, Task, Action, Result and return details"""
    text = answer.lower()
    present = {part: any(cue in text for cue in cues) for part, cues in STAR_CUES.items()}
    covered = sum(present.values())
    return {
        "components": present,              # {"situation": True, "task": False, ...}
        "missing": [p for p, ok in present.items() if not ok],
        "star_score": covered * 25,         # 0, 25, 50, 75, 100
        "is_star": covered == 4,            # your "75%" threshold idea fits here
    }

def score_relevance(answer: str, expected_keywords: list[str]) -> dict:
    """scores (0–100) how many expected keywords/concepts for the question appear in the answer."""
    text = answer.lower()
    matched = [k for k in expected_keywords if k.lower() in text]
    missed  = [k for k in expected_keywords if k.lower() not in text]
    score = round(100 * len(matched) / max(len(expected_keywords), 1))
    return {
        "relevance_score": score,
        "matched_keywords": matched,
        "missing_keywords": missed,
    }