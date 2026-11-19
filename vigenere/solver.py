ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decrypt(ciphertext, key):
    plaintext = ""
    key_index = 0

    for i in range(len(ciphertext)):
        if ciphertext[i].upper() in ALPHABET:
            p = ALPHABET.index(ciphertext[i].upper())
            k = ALPHABET.index(key[key_index % len(key)].upper())
            c = (p - k) % 26

            plaintext += ALPHABET[c]
            key_index += 1
        else:
            plaintext += ciphertext[i]

    return plaintext


def main():
    ciphertext = input("ciphertext: ")
    key = input("key: ")
    print(decrypt(ciphertext, key))


if __name__ == "__main__":
    main()
