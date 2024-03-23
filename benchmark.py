import subprocess
import json
import time


def generate_ciphertexts(num_cases):
    ciphertexts = []
    plaintexts = []
    for _ in range(num_cases):
        # Call encryption_scheme.py and capture its output
        result = subprocess.run(['python3', 'encryption_scheme.py'], capture_output=True, text=True)
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
        result = subprocess.run(['python3', 'ahuja-todora-delossantos-decrypt-source.py'], input=ciphertext, capture_output=True, text=True)
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
    print(f"-----------------------------------------------------------------------------")
    print(f"Measuring the accuracy of the cracker...")
    print(f"-----------------------------------------------------------------------------")
    tot_accuracy = 0
    for i in range(0,10):
        num_cases = 10  # Number of cases for the benchmark
        plaintexts, ciphertexts = generate_ciphertexts(num_cases)
        # print(f"\nPlaintexts are: {plaintexts}")
        # print(f"\nCiphertexts are: {ciphertexts}")
        timeA = time.time()
        guessed_plaintexts = crack_ciphertexts(ciphertexts)
        timeB = time.time()
        # print(f"\nGuesses are: {guessed_plaintexts}")
        accuracy = calculate_accuracy(plaintexts, guessed_plaintexts)
        tot_accuracy += accuracy
        print(f"\tAccuracy of the cracker during iteration {i+1}: {accuracy}%. Avg Time: {round((timeB - timeA)/10, 3)} sec")
    print(f"-----------------------------------------------------------------------------")
    print(f"Total Accuracy of the cracker after 100 cracking attempts: {tot_accuracy/10}%")
    print(f"-----------------------------------------------------------------------------")


if __name__ == "__main__":
    main()
