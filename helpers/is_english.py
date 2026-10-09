import sys

with open("helpers/google-10000-english.txt", "r", encoding="utf-8") as file:
    common_words = set(file.read().lower().split())


def english_score(input_string):
    words = input_string.lower().split()
    score = 0
    for word in words:
        word = word.strip(".,!?;:'\"()[]")
        if word in common_words:
            score += len(word)
    return score


def main():
    plaintext = sys.argv[1]
    print(english_score(plaintext))


if __name__ == "__main__":
    main()
