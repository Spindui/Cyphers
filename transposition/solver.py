def decrypt(cipher_text, key):
    list_of_words = cipher_text.split()
    output_list_of_words = []

    for word in list_of_words:
        decrypted_word = ""

        for position in key:
            decrypted_word += word[position - 1]

        output_list_of_words.append(decrypted_word)

    return " ".join(output_list_of_words)


def main():
    cipher_text = input("Enter the ciphertext: ")
    key = [2, 4, 5, 1, 3]

    plaintext = decrypt(cipher_text, key)
    print("_________________")
    print("Answer: ")
    print(plaintext)


if __name__ == "__main__":
    main()
