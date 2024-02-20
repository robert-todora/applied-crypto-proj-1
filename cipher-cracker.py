#!/usr/bin/env python3

def guess_plaintext(cipher):
    return cipher

def main():
    cptext = input("Enter the ciphertext:")
    plaintext = guess_plaintext(cptext)
    print(f"Plaintext guess: {plaintext}")

if __name__ == '__main__': 
    main()
