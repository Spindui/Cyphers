ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_permutations(length):
    """Generate all possible keys of the given length."""
    if length < 1:
        raise ValueError("Key length must be at least 1.")

    permutations = []

    def generate(current):
        if len(current) == length:
            permutations.append(current)
            return

        for letter in ALPHABET:
            generate(current + letter)

    generate("")

    return permutations
