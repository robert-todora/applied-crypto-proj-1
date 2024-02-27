# P1
Project 1 for CS-GY 6903 Applied Cryptography at NYU Spring 2024

## Python Part
### cipher-cracker.py
> Program which will take a ciphertext as input, and output a plaintext guess

__Important considerations__
- The chosen cipher for these first tests is the __shift__ cipher (_we can change this, or even try more than one..._)
- There are the following strategies implemented:
  - Randomly choose a plaintext (_bad results_)
  - Frequency analysis (explained below) (_partial good results_)
  - Frequency analysis using bigrams (same as below but using bigrams (i.e., AA, AB, AC...) instead of chars) (_bad results_)
  - [IoC][(https://en.wikipedia.org/wiki/Index_of_coincidence)] (_bad results_)
  - [X-gram Statistics as a Fitness Measure][http://www.practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/#a-python-implementation] (_huge results_)

__Frequency Analysis Technique__
- The implemented logic consists of the following:
  - __Ciphertext work__
    - The frequency of each char of the ciphertext is calculated and stored (i.e., `[5, 8, 3, 2, ...]`) for a ciphertext where the char `a` appeared 5 times, `b` 8, `c` 3, etc.
    - This array is sorted to have something like `[8, 5, 3, 2, ...]`
  - __Plaintext work__
    - Same as before, we get 5 sorted arrays with the frequencies of each of the plaintexts
  - __Distributions comparison__
    - Now the frequencies of each plaintext is compared with the one of the ciphertext
    - A `score` value for each case is calculated
      - If the length of the sorted array is not the same (i.e., one text did not have any occurrence of one char), we add a `0` to the end to be able to compare both distributions equally.
      - The score will be based in the absolute value of the subtraction of each value of the frequency in the same position.
        - That is, for two distributions like `[3, 2, 1]` and `[3, 2, 1]` the score will be __0__.
        - And for  `[3, 2, 1]` and `[3, 2, 2]` the score will be __1__.
      - After calculating every score, the lowest score will determine the best guess.

__X-Grams + Levenshtein Technique__
#### Sources
- The following links are the main sources from where I extracted all the info to implement this technique:
  - [Cryptanalysis of the Caesar Cipher][http://www.practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-caesar-cipher/]
  - [Main page][http://www.practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/#a-python-implementation]
  - [Monograms File][http://www.practicalcryptography.com/media/cryptanalysis/files/english_monograms.txt]
  - [Bigrams File][http://www.practicalcryptography.com/media/cryptanalysis/files/english_bigrams.txt]
  - [Score Calculation][http://www.practicalcryptography.com/media/cryptanalysis/files/ngram_score_1.py]
  - [Breaking Caesar][http://www.practicalcryptography.com/media/cryptanalysis/files/break_caesar_4.py]
#### Explanation
- Very briefly, first, we downloaded the Monograms and Bigrams dictionary. These are files with the different monograms and bigrams found in the English language followed by a number depending on their probability of occurrence.
- We implemented the `NgramScore` Python Class, where the goal is first, in the `init` function, to calculate the log probabilities of the dictionary passed as an argument (we are just using monograms or bigrams now, not both)
- Second, implement a `score` function to use the previous information to compare with a passed text.
- Lastly, we implement a `break_caesar` function, to use the previous code to guess the potential key used to encrypt a message with the `shift` cipher.
- Now, once we have the potential `key`, we attempt to decrypt the `ciphertext` to obtain a `plaintext`, including its random chars.
- Now, the last step is to decide which one of the texts in our `ptext_dict` is equivalent to the potential plaintext guessed with the obtained key. To do that, we use [Levenshtein Distance][https://en.wikipedia.org/wiki/Levenshtein_distance]
- Levenshtein Distance is the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word (in this case, text) into the other.
- With this, we select our plaintext guess and we output it from our cracker.

__Results__
- The previous explained techniques had the following results depending on the value of `prob_of_random_ciphertext` (the probability of one character of the ciphertext being random), using 10 cases, and 5 plaintexts of length L=600:
  | Randomness   | Frequency Analysis Accuracy  | X-Grams + Levenshtein Accuracy|
  |--------------|------------------------------|-------------------------------|
  | 0            | __100%__ :white_check_mark:  | __100%__ :white_check_mark:   |
  | 5            | __100%__ :white_check_mark:  | __100%__ :white_check_mark:   |
  | 10           | __100%__ :white_check_mark:  | __100%__ :white_check_mark:   |
  | 15           | __50%__ :x:                  | __100%__ :white_check_mark:   |
  | 20           | __20%__ :x:                  | __100%__ :white_check_mark:   |
  | 25           | __10%__ :x:                  | __100%__ :white_check_mark:   |
  | 30           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 35           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 40           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 45           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 50           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 55           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 60           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 65           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 70           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 75           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 80           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 85           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 90           | N/A :x:                      | __100%__ :white_check_mark:   |
  | 95           | N/A :x:                      | __80%__ :small_orange_diamond:|
  | 99           | N/A :x:                      | __35%__ :x:                   |

---
### encryption_scheme.py
> Program which will cipher a plaintext using a shift cipher with a random generated key and a hardcoded value of `prob_of_random_ciphertext`

__Important considerations__
- The logic follows the approached shown in the pseudo-code given by the Professor in Brightspace
- We are __not encrypting__ the blank `' '` character.

__Logic__
- We have the `plaintext_dict` of 5 texts, a random key in each execution (amount of characters shifted, i.e., ROT-key; `a` will be `b` if `key=1`, and `c` if `key=2`, etc.), and the `prob_of_random_ciphertext`.
- We randomly select one of the plaintexts from the dict.
- We encrypt it. To do that:
  - If a random "coin toss" says so, we insert a random character instead of encrypting.
  - Otherwise, we apply the shift cipher.
    - Logic here in the code can be a bit confusing since we don't assume the key length is 1, so we can use this same approach for cipher schemes which require longer keys.
---
### benchmark.py
> Program to test the accuracy of our cipher cracker. It will generate a hardcoded number of `cases`, where it will cipher a random plaintext using `encryption_scheme.py`, and then try to guess the plaintext ciphered calling `cipher-cracker.py`. It will output the percentage of accuracy of the guesses.

__Logic__
- We select the number of cases to test.
- We generate that same amount of ciphertexts.
  - We do this calling to `encryption_scheme.py`
  - And correctly parsing its output to gather the ciphertexts with their correspondent plaintexts
  - We store both in an array of arrays with the form `[plaintexts, ciphertexts]`. I.e., `[[p1, p2, ...], [c1, c2, ...]]`
- We try to crack every generated ciphertext
  - We do this calling our `cipher-cracker.py`
  - And correctly parsing its output to gather the guesses
  - We store these in an array with the form `[ptextguess1, ptextguess2, ...]`
- We calculate the accuracy of our guesses
  - We compare our guesses with the original plaintexts, i.e., `[ptextguess1, ptextguess2, ...]` with `[p1, p2, ...]`
  - We add the correct guesses and calculate the percentage of accuracy
  - We output this value as the only output of our `benchmark.py`

## C Part
> We just have a very basic skeleton as a starting point.
> Maybe we should end up submitting a final C project in case there's a big difference with Python in terms of efficiency

## TODO
1. Choose cipher we want to try to reverse
  * __shift__ ?
2. Code is a mess right now, improve how it looks

## IDEAS
1. Implement more than one for extra credit? We could do this by having a command line option to choose the cipher type we want to try to reverse
2. Use C for efficiency
3. Use concurrency or parallelism for efficiency
4. What if we use the length of the ciphertexts to infer the randomness chosen and apply one or other method to be more efficient.
5. Weighting Scheme to apply different techniques and get to a final decision.

## QUESTIONS
1. Should we encrypt the space/blank `' '` character as well?
2. Can we use the length of the ciphertext as information?
3. Not all the words from the texts are in the English dictionary...
