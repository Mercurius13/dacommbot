import random
import os

key = os.environ['key']
alphabet = os.environ['alphabet']

def decrypt_text(encrypted_text):
    def key_subs_decode(encrypted_text, key, alphabet):
        keyMap = dict(zip(key, alphabet))
        return ''.join(keyMap.get(c, c) for c in encrypted_text)


    def CaesarDecode(encrypted_text):
        shiftAmt = 8

        outputText = ""
        for char in encrypted_text:
            charPosition = ord(char)
            if 48 <= charPosition <= 57:
                newCharPosition = (charPosition - 48 - shiftAmt) % 10 + 48
            elif 65 <= charPosition <= 90:
                newCharPosition = (charPosition - 65 - shiftAmt) % 26 + 65
            elif 97 <= charPosition <= 122:
                newCharPosition = (charPosition - 97 - shiftAmt) % 26 + 97
            else:
                newCharPosition = charPosition
            outputText += chr(newCharPosition)

        return outputText

    decrypt_level_4 = encrypted_text[::-1]
    decrypt_level_3 = decrypt_level_4.replace('/', '')
    decrypt_level_3 = decrypt_level_3.replace('|', '')
    decrypt_level_3 = decrypt_level_3.replace('~', '')
    decrypt_level_3 = decrypt_level_3.replace('^', '')
    cipher_caesar_shift = decrypt_level_3.replace('`', '')

    decrypt_level_1 = CaesarDecode(cipher_caesar_shift)
    decrypt_level_2 = key_subs_decode(decrypt_level_1, key, alphabet)
    final_decrypted_text = decrypt_level_2
    return final_decrypted_text