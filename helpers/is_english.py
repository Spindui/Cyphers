# Common English quadgrams.
# These are illustrative weights; a full frequency
# table will produce much better results.

QUADGRAMS = {
    "TION": 100,
    "THER": 95,
    "THAT": 90,
    "OFTH": 85,
    "FTHE": 85,
    "THES": 80,
    "WITH": 80,
    "ATIO": 75,
    "MENT": 75,
    "HERE": 70,
    "OULD": 70,
    "IGHT": 70,
    "HAVE": 70,
    "HICH": 65,
    "WHIC": 65,
    "THIS": 65,
    "THEN": 65,
    "THEY": 60,
    "EVER": 60,
    "FROM": 60,
    "TING": 60,
    "ANCE": 55,
    "EDTH": 55,
    "WERE": 55,
    "IONS": 55,
    "THEM": 50,
    "INTH": 50,
    "ANDT": 50,
    "DTHA": 45,
}


def english_score(text):
    text = "".join(char for char in text.upper() if char.isalpha())

    score = 0

    for i in range(len(text) - 3):
        quadgram = text[i : i + 4]

        if quadgram in QUADGRAMS:
            score += QUADGRAMS[quadgram]

    return score
