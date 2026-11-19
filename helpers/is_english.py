from pathlib import Path

WORD_LIST = Path(__file__).with_name("google-10000-english.txt")

with WORD_LIST.open("r", encoding="utf-8") as file:
    COMMON_WORDS = set(file.read().lower().split())


def english_score(input_string):
    words = input_string.lower().split()
    score = 0

    for word in words:
        word = word.strip(".,!?;:'\"()[]")
        if word in COMMON_WORDS:
            score += len(word)

    return score
