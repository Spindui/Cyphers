ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def index_of_coincidence(text):
    counts = [0] * 26

    for char in text:
        if char in ALPHABET:
            counts[ALPHABET.index(char)] += 1

    total = sum(counts)

    if total < 2:
        return 0

    numerator = sum(count * (count - 1) for count in counts)

    return numerator / (total * (total - 1))


def key_length(ciphertext):
    ciphertext = "".join(char for char in ciphertext.upper() if char in ALPHABET)

    results = []

    for period in range(1, 16):
        slices = [""] * period

        for i, char in enumerate(ciphertext):
            slices[i % period] += char

        average_ioc = sum(index_of_coincidence(s) for s in slices) / period

        results.append((period, average_ioc))

        print(f"Key length {period}: {average_ioc:.4f}")

    best = max(results, key=lambda x: x[1])

    return best[0]


def main():
    ciphertext = input("Enter ciphertext: ")
    print("Possible key length:", key_length(ciphertext))


if __name__ == "__main__":
    main()
