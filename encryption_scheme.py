#!/usr/bin/env python3
import random

# Define the character set for the message and ciphertext.
# Just lowercase chars
CHARACTER_SET = [chr(i) for i in range(ord('a'), ord('z') + 1)]

# Classic Caesar cipher
def shift_cipher(character, shift):
    if character not in CHARACTER_SET:
        return character
    index = (CHARACTER_SET.index(character) + shift) % len(CHARACTER_SET)
    return CHARACTER_SET[index]

def coin_generation_algorithm(ciphertext_pointer, t, L):
    # Simple random coin generation algorithm for demonstration
    return random.random()

def encrypt_message(message, key, prob_of_random_ciphertext):
    ciphertext = ""
    ciphertext_pointer = 1
    message_pointer = 1
    num_rand_characters = 0
    L = len(message)

    while ciphertext_pointer <= L + num_rand_characters:
        coin_value = coin_generation_algorithm(ciphertext_pointer, len(key), L)

        if prob_of_random_ciphertext <= coin_value <= 1:
            j = (message_pointer % len(key)) + 1
            ciphertext += shift_cipher(message[message_pointer - 1], key[j - 1])
            message_pointer += 1

        elif 0 <= coin_value < prob_of_random_ciphertext:
            random_character = random.choice(CHARACTER_SET)
            ciphertext += random_character
            num_rand_characters += 1

        ciphertext_pointer += 1

    return ciphertext

# Example usage
# Plaintext dictionary with five candidate plaintexts
ptext_dict = [
    "unconquerable tropical pythagoras rebukingly price ephedra barmiest hastes spades fevers cause wisped overdecorates linked smitten trickle scanning cognize oaken casework significate influenceable precontrived clockers defalcation fruitless splintery kids placidness regenerate harebrained liberalism neuronic clavierist attendees matinees prospectively bubbies longitudinal raving relaxants rigged oxygens chronologist briniest tweezes profaning abeyances fixity gulls coquetted budgerigar drooled unassertive shelter subsoiling surmounted frostlike jobbed hobnailed fulfilling jaywalking testabilit",
    "protectorates committeemen refractory narcissus bridlers weathercocks occluding orchectomy syncoms denunciation chronaxy imperilment incurred defrosted beamy opticopupillary acculturation scouting curiousest tosh preconscious weekday reich saddler politicize mercerizes saucepan bifold chit reviewable easiness brazed essentially idler dependable predicable locales rededicated cowbird kvetched confusingly airdrops dreggier privileges tempter anaerobes glistened sartorial distrustfulness papillary ughs proctoring duplexed pitas traitorously unlighted cryptographer odysseys metamer either meliorat",
    "incomes shoes porcine pursue blabbered irritable ballets grabbed scything oscillogram despots pharynxes recompensive disarraying ghoulish mariachi wickerwork orientation candidnesses nets opalescing friending wining cypher headstrong insubmissive oceanid bowlegs voider recook parochial trop gravidly vomiting hurray friended uncontestable situate fen cyclecars gads macrocosms dhyana overruns impolite europe cynical jennet tumor noddy canted clarion opiner incurring knobbed planeload megohm dejecting campily dedicational invaluable praecoces coalescence dibbuk bustles flay acuities centimeters l",
    "rejoicing nectar asker dreadfuls kidnappers interstate incrusting quintessential neglecter brewage phosphatic angle obliquely bean walkup outflowed squib tightwads trenched pipe extents streakier frowning phantasmagories supinates imbibers inactivates tingly deserter steerages beggared pulsator laity salvageable bestrode interning stodgily cracker excisions quanted arranges poultries sleds shortly packages apparat fledge alderwomen halvah verdi ineffectualness entrenches franchising merchantability trisaccharide limekiln sportsmanship lassitudes recidivistic locating iou wardress estrus potboi",
    "headmaster attractant subjugator peddlery vigil dogfights pixyish comforts aretes felinities copycat salerooms schmeering institutor hairlocks speeder composers dramatics eyeholes progressives reminiscent hermaphrodism simultaneous spondaics hayfork armory refashioning battering darning tapper pancaked unaffected televiewer mussiness pollbook sieved reclines restamp cohosh excludes homelier coacts refashioned loiterer prospectively encouragers biggest pasters modernity governorships crusted buttoned wallpapered enamors supervisal nervily groaning disembody communion embosoming tattles pancakes"
]
# Generate a random key for the shift cipher
key = [random.randint(0, 26)]  # Random shift value between 0 and 26
prob_of_random_ciphertext = 0.05  # Chance of inserting a random character

# Encrypt a random plaintext from the dictionary
random_plaintext = random.choice(ptext_dict)
# --- DELETE LATER
# Manually choosuing the plaintext for testing purposes
# key = [1]
# random_plaintext = ptext_dict[0]
# ---
ciphertext = encrypt_message(random_plaintext, key, prob_of_random_ciphertext)
print(f"\nPlaintext: {random_plaintext}")
print(f"\nKey: {key}")
print(f"\nCiphertext: {ciphertext}")
