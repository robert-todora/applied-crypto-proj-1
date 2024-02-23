#!/usr/bin/env python3
import random

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

    '''
    # Normalize frequencies to percentages
    total_letters = sum(frequency.values())
    for letter in frequency:
        frequency[letter] = frequency[letter] / total_letters
    '''

    return frequency

def get_sorted_frequencies(frequency):
    return sorted(frequency.values(), reverse=True)

def compare_distributions(ctext_freq_sorted, ptext_freq_sorted):
    # Comparing the length of the frequency lists first
    if len(ctext_freq_sorted) != len(ptext_freq_sorted):
        return float('inf') # Initialize with infinite

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

def random_guess_plaintext():
    # Randomly select one of the plaintexts from the dictionary
    random_index = random.randint(0, len(ptext_dict) - 1)
    return ptext_dict[random_index]

def guess_plaintext(ctext):
    # guess = random_guess_plaintext()
    guess = frequency_guess_plaintext(ctext)
    return guess

def main():
    ctext = input("Enter the ciphertext:")
    ptext = guess_plaintext(ctext)
    print(f"\nMy plaintext guess is: {ptext}")

if __name__ == '__main__':
    main()
