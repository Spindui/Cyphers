import sys
from collections import Counter


def find_letter_frequency(input_string):
    letter_count = Counter()

    for char in input_string.upper():
        if char.isalpha():
            letter_count[char] += 1

    return letter_count


def display_frequencies(frequencies):
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(f"{letter}: {frequencies[letter]}")


def main():
    input_string = sys.argv[1]
    frequencies = find_letter_frequency(input_string)
    display_frequencies(frequencies)


if __name__ == "__main__":
    main()
