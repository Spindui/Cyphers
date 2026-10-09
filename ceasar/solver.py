import sys
from helpers.is_english import english_score


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


def solver(input_string, amount_of_results):
    candidates = []

    for shift_amount in range(26):
        shifted_string = shift(input_string, shift_amount)
        score = english_score(shifted_string)
        candidates.append((score, shift_amount, shifted_string))

    return sorted(candidates, reverse=True)[0:amount_of_results]


def main():
    cipher_text = sys.argv[1]
    amount_of_results = int(sys.argv[2])

    answers = solver(cipher_text, amount_of_results)

    for score, shift_amount, answer in answers:
        print(f"Shift: {shift_amount}")
        print(f"Score: {score}")
        print(f"Plaintext: {answer}")
        print("----------------")


if __name__ == "__main__":
    main()
