import random
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('key')
alphabet = os.getenv('alphabet')

def encrypt_text(plaintext):
    first_j = False
    if plaintext.startswith('j'):
        first_j = True
    def makeKey(alphabet):  # needed only while making new key
        alphabet = list(alphabet)
        random.shuffle(alphabet)
        return ''.join(alphabet)

    def key_subs_encode(plaintext, key, alphabet):
        keyMap = dict(zip(alphabet, key))
        return ''.join(keyMap.get(c, c) for c in plaintext)

    def CaesarEncode(inputText):
        shiftAmt = 8

        cipherText = ""
        for char in inputText:
            charPosition = ord(char)
            if 48 <= charPosition <= 57:
                newCharPosition = (charPosition - 48 + shiftAmt) % 10 + 48
            elif 65 <= charPosition <= 90:
                newCharPosition = (charPosition - 65 + shiftAmt) % 26 + 65
            elif 97 <= charPosition <= 122:
                newCharPosition = (charPosition - 97 + shiftAmt) % 26 + 97
            else:
                newCharPosition = charPosition
            cipherText += chr(newCharPosition)

        return cipherText

    cipher_key_subs = key_subs_encode(plaintext, key, alphabet)
    cipher_caesar_shift = CaesarEncode(cipher_key_subs)
    lst = ["/", "|", "~", "^", "`"]
    string = cipher_caesar_shift

    encrypt3 = (''.join(f"{x}{random.choice(lst) if random.randint(0, 4) else ''}" for x in string))
    encrypt4 = encrypt3[::-1]
    if first_j is False:
        final_encrypted_text = encrypt4
    else:
        final_encrypted_text = encrypt4 + random.choice(lst)
    return final_encrypted_text
