"""T-2904: write a generated file only when its content changes, so rerunning a port or build leaves no churn."""
import os


def write_if_changed(path, text):
    """True when path was (re)written, False when it already held text."""
    try:
        with open(path, encoding="utf-8") as f:
            if f.read() == text:
                return False
    except FileNotFoundError:
        pass
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return True
