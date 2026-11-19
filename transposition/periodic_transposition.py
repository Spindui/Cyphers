import re
import random
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers.is_english import english_score


CIPHERTEXT = """
RTOOHHUUAAFRDRNOERKRAYYYTSENETSORCSTLIOIEMNATUFMIUEMRRDREPTEELRHNYIATSSTTCOGHIDAADIRLSESIDDROETEATIHDHHEVOOMDIUPMCGEYEHDTHTTHEEEACSLIVOYGEUTHTROSESUOLUFHFRILIIEMMAYESMOIPCRSEEAINABNNDDDDEMHENIUNLHTOTEITORLTAGEINEBSATVTASETRUNRERCIAYOEIONNTUHQIRAUEESASLETLWHHIEEETAIISENSEIGUTSOFPHOOPEKRORYYDTOTOHNOUOOEFTNWIALANLIIOQFSSUEPEIUARDGROEHHPNSRLOMAEDATSURYHSIBEPEERRVHIREENRTIEACHMSTAAIINGADHHHFOSOOREFNROAGAURETGCSPEOTRSWUEFITDMOHIILEOSLHOFSEVTSDEHINIREGSYMTCOIOPPUOAALTYRANAITGGNIFEGCTNEEETQNNOUTRTTIAIHPTOEMDPRUBHANYOPIUTTHSHOIEEGCACOETHMDSWPYTEALTASEHRCTENRARDEYDITTEARTSYEOTAGSNRSIETSLIHIMHTENAHMGTEIFCHRFKEAONCURSOASTRMEOTEDMGNSISCBSEEETSQSHIUHENEAOEOEUSMMNTAEEDUNNTDAFHIGSMTESEHRUTEANRHCTEAAASTMNNUEOSTPTEFAHBNOAETRSEORNEAADSBCNELCIOEEROMTANSOTSPCFDEEOIAIORSRUIAANTPNDOROTNARHSBEFIILISDYNCEMTGHOUTEFRHLTDBAOIINSSNTSIEWMLLIEMFLMHIYLETORFSUETERAHLFTAEOTBTTUETTNRHEDAAGEMNIFESNEHRLGEAOSCMDRDOMDTRKTOEEHRARYRSOAETONCOEEOFQNVSUTEEOIRRMPEYEMDETIADHPSTEMISHEHUAQAMTUBEEREDMILTYOEOOSNNTTTGHEEARENDNCWSEAUHUDSOBTMHOHATGGMIITAANOMNMNEBBIRUENDTEAEHCIREATWWRMOHTENEHRFAWQWTAUATNISSHTEWEELHYDHSGMYHOUTOTCTHUOEELSWYDOOOEAURRGBEAEHLCDTEOARTVMMEIPENLRRTMEDAHWCWEAAHFSAEEOBICTLRTASYOIUTBSMHJNLARSCSEQLFLUTEOIAAROLRMTIUNEOTEDNTXSEAHPSBEOTOUSPETRITITAHSITGAARRTPIEIAAREORIAFLOTTCYUUUCSRLUFEAEEUSRSLETSDHNHIEEEWCVLOENNTLTCHUTLABCOUETCDRAOETARMHSRPEOELTFCDNTCSOHUICHEEAENSUECNYSVEBEIDETDOINEATIXTOTPIOUILTRAAFILNHIETENRHMGAEOICMNSAATSMNENEHAGRETLADTEENHNTDRITTPNHRPCEAEECAIAOASRFMAATELOTDLUENSSREREMSERAAAITNOLIMBASAEIHKEENADXELTPDLREROANMTNTRTEGSEAEFLRMOIVSEIESTCATEAOCOCHCTHAEHNAOSEFNISFANELARCSTCETMHHDIPTENUHTERIEEDSMRTUSMOENQSBEUHEOIOGSFRULEYLINIDEYLNFODDUURHRLWEAIOMTFUIHCNNARRSTEEEIDTMMIIATSOINHIATETTICITSAOOSLNNETDSELHRDMEATIAFAONICFGRHITCRUTNEARDULIWTNLCWUYTESSAVGIEEHCSEDUAENILHOFTAUFIAHEODOSBYUTELWTURITDETHIISTONUOFGBFTCTJOOHENMECEEORUERYRXDRSHTIUORNMSAAOTOLFSCAREITETEREHMCSATUOIYOINWUVHOKAEOONLLDOYLYWYDTAOGHNUEADLRMRUJEREUNYVSSGEHCENTOIIOOUHWDRAIIAIWTOAHIMTESPNIRAIVECTEICEOEEDDWRBSHMAYEENGNTIOSHISBAOEOLTSTIRPSHEOEQLSSUSNSHRSEAETELTMONIABIEIESMTEAOEDRSRTWLTEOBISHENTEHSVOEOIUMFSRHAHIAKITTESYNYAOCBHRERADSRERSENTILDF
"""

EXPECTED_LENGTH = 2112

# Small hand-manageable rectangles
MAX_DIMENSION = 10
MAX_BLOCK_SIZE = 100

RESTARTS = 5
STEPS = 500


def clean_text(text):
    return re.sub(r"[^A-Z]", "", text.upper())


def get_dimensions(length):
    """Find rectangular blocks whose area divides 2112."""

    dimensions = []

    for rows in range(2, MAX_DIMENSION + 1):
        for cols in range(2, MAX_DIMENSION + 1):
            block_size = rows * cols

            if block_size > MAX_BLOCK_SIZE:
                continue

            if length % block_size == 0:
                dimensions.append((rows, cols, block_size))

    return sorted(dimensions, key=lambda x: (x[2], x[0], x[1]))


def decrypt_block(block, rows, cols, order):
    """
    Reconstruct a rectangle.

    The encrypted block was read column by column,
    after its columns were shuffled.

    order maps ciphertext column positions
    back to their original column positions.
    """

    columns = [""] * cols

    for position, original_column in enumerate(order):
        start = position * rows
        end = start + rows

        columns[original_column] = block[start:end]

    plaintext = ""

    for row in range(rows):
        for col in range(cols):
            plaintext += columns[col][row]

    return plaintext


def decrypt_message(ciphertext, rows, cols, order):

    block_size = rows * cols
    plaintext = []

    for start in range(0, len(ciphertext), block_size):
        block = ciphertext[start : start + block_size]

        plaintext.append(decrypt_block(block, rows, cols, order))

    return "".join(plaintext)


def improve_order(ciphertext, rows, cols):

    # Generate a random starting permutation.
    current_order = list(range(cols))
    random.shuffle(current_order)

    current_plaintext = decrypt_message(ciphertext, rows, cols, current_order)

    current_score = english_score(current_plaintext)

    best_order = current_order[:]
    best_plaintext = current_plaintext
    best_score = current_score

    for step in range(STEPS):
        candidate_order = current_order[:]

        # Swap two randomly selected columns.
        a, b = random.sample(range(cols), 2)

        candidate_order[a], candidate_order[b] = (
            candidate_order[b],
            candidate_order[a],
        )

        candidate_plaintext = decrypt_message(ciphertext, rows, cols, candidate_order)

        candidate_score = english_score(candidate_plaintext)

        # Gradually reduce the temperature.
        temperature = 50 * (1 - step / STEPS) + 2

        difference = candidate_score - current_score

        # Accept improvements or occasionally accept
        # worse solutions to escape local maxima.
        if difference > 0 or random.random() < math.exp(difference / temperature):
            current_order = candidate_order
            current_score = candidate_score

        if current_score > best_score:
            best_score = current_score
            best_order = current_order[:]

            best_plaintext = decrypt_message(ciphertext, rows, cols, best_order)

    return best_score, best_order, best_plaintext


def solve(ciphertext):

    dimensions = get_dimensions(len(ciphertext))

    print("\nPOSSIBLE BLOCK DIMENSIONS")
    print("=" * 45)

    for rows, cols, size in dimensions:
        print(f"{rows} x {cols} = {size} characters | {len(ciphertext) // size} blocks")

    results = []

    print("\nSTARTING SEARCH")
    print("=" * 45)

    for rows, cols, size in dimensions:
        print(f"\nTesting {rows} rows x {cols} columns")

        best_score = float("-inf")
        best_order = None
        best_plaintext = None

        for restart in range(RESTARTS):
            score, order, plaintext = improve_order(ciphertext, rows, cols)

            if score > best_score:
                best_score = score
                best_order = order
                best_plaintext = plaintext

            if (restart + 1) % 10 == 0:
                print(f"  Restart {restart + 1}/{RESTARTS} | Best score: {best_score}")

        result = {
            "score": best_score,
            "rows": rows,
            "cols": cols,
            "block_size": size,
            "order": best_order,
            "plaintext": best_plaintext,
        }

        results.append(result)

        print("\nBest result for this size:")
        print("Column order:", best_order)
        print("English score:", best_score)
        print("Plaintext:", best_plaintext[:200])

    # Rank all candidate dimensions.
    results.sort(key=lambda x: x["score"], reverse=True)

    print("\n\nTOP 10 RESULTS")
    print("=" * 60)

    for index, result in enumerate(results[:10], 1):
        print(f"\nRANK {index}")
        print("-" * 40)

        print(f"Block dimensions: {result['rows']} x {result['cols']}")

        print("Block size:", result["block_size"])
        print("Column order:", result["order"])
        print("English score:", result["score"])

        print("\nPlaintext:")
        print(result["plaintext"][:500])

    # Save the best candidate.
    if results:
        best = results[0]

        with open("best_plaintext.txt", "w", encoding="utf-8") as file:
            file.write(best["plaintext"])

        print("\nBest candidate saved to best_plaintext.txt")

    return results


def main():

    ciphertext = clean_text(CIPHERTEXT)

    print("PERIODIC BLOCK TRANSPOSITION SOLVER")
    print("=" * 45)

    print("Ciphertext length:", len(ciphertext))

    if len(ciphertext) != EXPECTED_LENGTH:
        raise ValueError(
            f"Expected {EXPECTED_LENGTH} characters, but received {len(ciphertext)}."
        )

    random.seed()

    solve(ciphertext)


if __name__ == "__main__":
    main()
