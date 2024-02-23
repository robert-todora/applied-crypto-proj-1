import subprocess
import json

def generate_ciphertexts(num_cases):
    ciphertexts = []
    plaintexts = []
    for _ in range(num_cases):
        # Call encryption_scheme.py and capture its output
        result = subprocess.run(['python', 'encryption_scheme.py'], capture_output=True, text=True)
        # print(f"\nResult after executing the cipher: {result}")
        output = result.stdout.strip()
        # print(f"\nStriping the result: {output}")
        # Split the output into lines and extract plaintext and ciphertext
        lines = output.split('\n')
        plaintext_line = next(line for line in lines if line.startswith('Plaintext: '))
        ciphertext_line = next(line for line in lines if line.startswith('Ciphertext: '))

        plaintext = plaintext_line.replace('Plaintext: ', '').strip()
        ciphertext = ciphertext_line.replace('Ciphertext: ', '').strip()

        ciphertexts.append(ciphertext)
        plaintexts.append(plaintext)
    return plaintexts, ciphertexts

def crack_ciphertexts(ciphertexts):
    guessed_plaintexts = []
    for ciphertext in ciphertexts:
        # Call cipher-cracker.py and pass the ciphertext
        result = subprocess.run(['python', 'cipher-cracker.py'], input=ciphertext, capture_output=True, text=True)
        guessed_plaintext = result.stdout.strip()
        lines = guessed_plaintext.split('\n')
        plaintext_line = next(line for line in lines if line.startswith('My plaintext guess is: '))
        guessed_plaintext = plaintext_line.replace('My plaintext guess is: ', '').strip()
        guessed_plaintexts.append(guessed_plaintext)
    return guessed_plaintexts

def calculate_accuracy(plaintexts, guessed_plaintexts):
    correct_guesses = sum(p == g for p, g in zip(plaintexts, guessed_plaintexts))
    accuracy = (correct_guesses / len(plaintexts)) * 100
    return accuracy

def main():
    num_cases = 10  # Number of cases for the benchmark
    plaintexts, ciphertexts = generate_ciphertexts(num_cases)
    # print(f"\nPlaintexts are: {plaintexts}")
    # print(f"\nCiphertexts are: {ciphertexts}")
    guessed_plaintexts = crack_ciphertexts(ciphertexts)
    # print(f"\nGuesses are: {guessed_plaintexts}")
    accuracy = calculate_accuracy(plaintexts, guessed_plaintexts)
    print(f"\nAccuracy of cipher-cracker: {accuracy}%")

if __name__ == "__main__":
    main()