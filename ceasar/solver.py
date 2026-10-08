import sys
from langdetect import detect, LangDetectException


def shift(input_string, shifts):
    output_string = ""
    for char in input_string:
        if char.isalpha():
            number = ord(char.upper()) - ord("A") + shifts
            number %= 26
            output_string += chr(ord("A") + number)
        else:
            output_string += char

    return output_string


def is_english(input_string):
    try:
        return detect(input_string) == "en"
    except LangDetectException:
        return False


def solver(input_string):
    correct_answers = []
    for shift_amount in range(26):
        shifted_string = shift(input_string, shift_amount)
        if is_english(shifted_string):
            correct_answers.append((shift_amount, shifted_string))
    return correct_answers


def main():
    cipher_text = sys.argv[1]
    answers = solver(cipher_text)

    for shift_amount, answer in answers:
        print(shift_amount, answer)
        print("----------------")


if __name__ == "__main__":
    main()
