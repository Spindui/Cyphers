from helpers.permutations import get_permutations
from helpers.is_english import english_score

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decrypt(ciphertext, key):
    """Decrypt ciphertext using a Vigenere key."""
    if not key or not key.isalpha():
        raise ValueError("Key must contain letters.")

    plaintext = ""
    key_index = 0
    key = key.upper()

    for char in ciphertext:
        if char.upper() in ALPHABET:
            cipher_index = ALPHABET.index(char.upper())
            key_shift = ALPHABET.index(key[key_index % len(key)])

            plain_index = (cipher_index - key_shift) % 26
            decrypted_char = ALPHABET[plain_index]

            if char.islower():
                decrypted_char = decrypted_char.lower()

            plaintext += decrypted_char
            key_index += 1
        else:
            plaintext += char

    return plaintext


def crack(ciphertext, key_length):
    """Find the most likely key using English scoring."""
    best_key = None
    best_plaintext = None
    best_score = -1

    for key in get_permutations(key_length):
        plaintext = decrypt(ciphertext, key)
        score = english_score(plaintext)

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score


def main():
    ciphertext = input("Ciphertext: ")
    length = int(input("Key length: "))

    key, plaintext, score = crack(ciphertext, length)

    print("\nBest key:", key)
    print("English score:", score)
    print("Decrypted text:", plaintext)


if __name__ == "__main__":
    main()
