from itertools import permutations
from helpers.is_english import english_score


def decrypt_block(cipher, width, key):
    rows = len(cipher) // width

    columns = [None] * width

    for encrypted_position, original_position in enumerate(key):
        start = encrypted_position * rows
        end = start + rows

        columns[original_position] = cipher[start:end]

    plaintext = ""

    for row in range(rows):
        for column in range(width):
            plaintext += columns[column][row]

    return plaintext


def decrypt(cipher_text, width, key):
    if len(cipher_text) % width != 0:
        return None

    return decrypt_block(cipher_text, width, key)


def brute_force(cipher_text):
    cipher_text = "".join(c for c in cipher_text.upper() if c.isalpha())

    results = []

    for width in range(2, 9):
        if len(cipher_text) % width != 0:
            continue

        print(f"Testing width: {width}")

        for key in permutations(range(width)):
            plaintext = decrypt(cipher_text, width, key)

            if plaintext is None:
                continue

            score = english_score(plaintext)

            results.append((score, width, key, plaintext))

    results.sort(reverse=True, key=lambda x: x[0])

    print("\nTOP 10 RESULTS\n")

    for score, width, key, plaintext in results[:10]:
        print("=" * 60)
        print("Score:", score)
        print("Width:", width)
        print("Key:", tuple(x + 1 for x in key))
        print("Plaintext:", plaintext[:500])
        print()


def main():
    cipher_text = input("Enter ciphertext: ")
    brute_force(cipher_text)


if __name__ == "__main__":
    main()
