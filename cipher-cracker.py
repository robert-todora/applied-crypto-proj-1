#!/usr/bin/env python3
import random, re
import Levenshtein
from math import log10
from pycipher import Caesar

# Plaintext dictionary with five candidate plaintexts
ptext_dict = [
    "unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
    "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
    "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
    "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
    "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
]


# Calculate each char frequency for a given text
def calculate_frequency_distribution(text):
    frequency = {}
    for letter in text.lower():  # Convert to lowercase
        if letter.isalpha():  # Consider only alphabetic characters
            frequency[letter] = frequency.get(letter, 0) + 1
    return frequency


def get_sorted_frequencies(frequency):
    return sorted(frequency.values(), reverse=True)


def compare_distributions(ctext_freq_sorted, ptext_freq_sorted):
    # Pad the shorter list with zeros to match the length of the longer list
    length_difference = abs(len(ctext_freq_sorted) - len(ptext_freq_sorted))
    if len(ctext_freq_sorted) > len(ptext_freq_sorted):
        ptext_freq_sorted.extend([0] * length_difference)
    else:
        ctext_freq_sorted.extend([0] * length_difference)

    # Calculate the score based on the difference in frequencies
    score = sum(abs(a - b) for a, b in zip(ctext_freq_sorted, ptext_freq_sorted))
    return score


def frequency_guess_plaintext(ctext):
    ctext_freq = calculate_frequency_distribution(ctext)
    ctext_freq_sorted = get_sorted_frequencies(ctext_freq)

    best_match = None
    lowest_score = float('inf') # Initialize with infinite

    for plaintext in ptext_dict:
        ptext_freq = calculate_frequency_distribution(plaintext)
        ptext_freq_sorted = get_sorted_frequencies(ptext_freq)
        score = compare_distributions(ctext_freq_sorted, ptext_freq_sorted)

        if score < lowest_score:
            lowest_score = score
            best_match = plaintext

    return best_match


def guess_plaintext(ctext):
    # guess = random_guess_plaintext() # No good results
    guess = frequency_guess_plaintext(ctext) # Partial good results
    # guess = bigram_guess_plaintext(ctext)  # # No good results
    # guess = ioc_guess_plaintext(ctext) # No good results
    return guess


class NgramScore(object):
    def __init__(self, ngramfile, sep=' '):
        ''' Load a file containing ngrams and counts, calculate log probabilities '''
        self.ngrams = {}
        with open(ngramfile) as file:  # Use 'with' for proper file handling
            for line in file:
                key, count = line.split(sep)
                self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())  # Use .values() for Python 3
        # Calculate log probabilities
        for key in self.ngrams:
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)
        self.floor = log10(0.01 / self.N)


    def score(self, text):
        ''' Compute the score of text '''
        score = 0
        ngrams = self.ngrams.get  # Use .get for Python 3
        for i in range(len(text) - self.L + 1):  # Use range instead of xrange for Python 3
            score += ngrams(text[i:i+self.L], self.floor)  # Use ngrams.get with default value
        return score


def break_caesar(ctext, fitness):
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ctext = re.sub('[^a-z]','',ctext.lower())
    # try all possible keys, return the one with the highest fitness
    scores = []
    for i in range(26):
        scores.append((fitness.score(Caesar(i).decipher(ctext)),i))
    return max(scores)


CHARACTER_SET = [chr(i) for i in range(ord('a'), ord('z') + 1)]


def decrypt_shift_cipher(text, shift):
    decrypted_text = ""
    for character in text:
        if character in CHARACTER_SET:
            index = (CHARACTER_SET.index(character) - shift) % len(CHARACTER_SET)
            decrypted_character = CHARACTER_SET[index]
        else:
            decrypted_character = character
        decrypted_text += decrypted_character
    return decrypted_text


def find_equivalent_text(guessed_text, ptext_list):
    min_distance = float('inf')
    equivalent_text_index = None

    for index, original_text in enumerate(ptext_list):
        distance = Levenshtein.distance(guessed_text, original_text)
        if distance < min_distance:
            min_distance = distance
            equivalent_text_index = index

    return equivalent_text_index


def main():
    ctext = input("\nEnter the ciphertext:")
    fitness = NgramScore('bigrams.txt')
    # print(f'\nFitness score ctext {fitness.score(ctext)}')
    value, guess_key = break_caesar(ctext, fitness)
    # print(f'\nGuessed key: {guess_key}')
    guessed_text = decrypt_shift_cipher(ctext, guess_key)
    # print(f'\nGuessed text: {guessed_text}')

    equivalent_text_key = find_equivalent_text(guessed_text, ptext_dict)
    print(f"\nMy plaintext guess is: {ptext_dict[equivalent_text_key]}")


if __name__ == '__main__':
    main()
