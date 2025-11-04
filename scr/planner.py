import re

def parse_query(text: str):
    """
    Parse a natural-language query and identify user intent.
    Supported intents:
      - compare_rainfall_and_top_crops
      - district_max_crop
      - trend_and_correlation
    """
    t = text.lower().strip()

    # === Compare rainfall and crops between two states ===
    m = re.search(
        r"(?:compare|show|analyze)\s+(?:the\s+)?(?:average\s+)?(?:annual\s+)?rainfall.*?\s+in\s+([\w\s]+)\s+(?:and|vs)\s+([\w\s]+).*?(?:last|past)?\s*(\d+)?\s*(?:years)?",
        t,
    )
    if m:
        s1 = m.group(1).strip().title()
        s2 = m.group(2).strip().title()
        n = int(m.group(3)) if m.group(3) else 5  # Default to last 5 years
        return {
            "intent": "compare_rainfall_and_top_crops",
            "state_x": s1,
            "state_y": s2,
            "year_num": n,
        }

    # === Find highest/lowest producing district for a crop ===
    m = re.search(
        r"(?:find|identify|show)\s+(?:the\s+)?(?:district\s+in\s+)?([\w\s]+)\s+(?:with\s+)?(?:highest|maximum)\s+(?:production\s+of\s+)?([\w\s]+)",
        t,
    )
    if m:
        state = m.group(1).strip().title()
        crop = m.group(2).strip().title()
        return {
            "intent": "district_max_crop",
            "state": state,
            "crop": crop,
        }

    # === Analyze crop production trend and correlation ===
    m = re.search(
        r"(?:analyze|show|study)\s+(?:the\s+)?(?:trend\s+of\s+)?([\w\s]+)\s+(?:production\s+in\s+)?([\w\s]+).*?(?:last|past)?\s*(\d+)?\s*(?:years)?",
        t,
    )
    if m:
        crop = m.group(1).strip().title()
        state = m.group(2).strip().title()
        n = int(m.group(3)) if m.group(3) else 10  # Default to last 10 years
        return {
            "intent": "trend_and_correlation",
            "crop": crop,
            "state": state,
            "year_num": n,
        }

    # === Fallback ===
    return {
        "intent": "unknown",
        "raw_text": text,
    }
