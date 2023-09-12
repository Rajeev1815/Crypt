import streamlit as st

# Function to convert the string to lowercase
def toLowerCase(text):
    return text.lower()

# Function to remove all spaces in a string
def removeSpaces(text):
    newText = ""
    for i in text:
        if i == " ":
            continue
        else:
            newText = newText + i
    return newText

# Function to group 2 elements of a string as a list element
def Diagraph(text):
    Diagraph = []
    group = 0
    for i in range(2, len(text), 2):
        Diagraph.append(text[group:i])

        group = i
    Diagraph.append(text[group:])
    return Diagraph

# Function to fill a letter in a string element if 2 letters in the same string match
def FillerLetter(text):
    k = len(text)
    if k % 2 == 0:
        for i in range(0, k, 2):
            if text[i] == text[i + 1]:
                new_word = text[0:i + 1] + str('x') + text[i + 1:]
                new_word = FillerLetter(new_word)
                break
            else:
                new_word = text
    else:
        for i in range(0, k - 1, 2):
            if text[i] == text[i + 1]:
                new_word = text[0:i + 1] + str('x') + text[i + 1:]
                new_word = FillerLetter(new_word)
                break
            else:
                new_word = text
    return new_word

list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Function to generate the 5x5 key square matrix
def generateKeyTable(word, list1):
    key_letters = []
    for i in word:
        if i not in key_letters:
            key_letters.append(i)

    compElements = []
    for i in key_letters:
        if i not in compElements:
            compElements.append(i)
    for i in list1:
        if i not in compElements:
            compElements.append(i)

    matrix = []
    while compElements != []:
        matrix.append(compElements[:5])
        compElements = compElements[5:]

    return matrix

def search(mat, element):
    for i in range(5):
        for j in range(5):
            if (mat[i][j] == element):
                return i, j

def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    if e1c == 4:
        char1 = matr[e1r][0]
    else:
        char1 = matr[e1r][e1c + 1]

    char2 = ''
    if e2c == 4:
        char2 = matr[e2r][0]
    else:
        char2 = matr[e2r][e2c + 1]

    return char1, char2

def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    if e1r == 4:
        char1 = matr[0][e1c]
    else:
        char1 = matr[e1r + 1][e1c]

    char2 = ''
    if e2r == 4:
        char2 = matr[0][e2c]
    else:
        char2 = matr[e2r + 1][e2c]

    return char1, char2

def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    char1 = ''
    char1 = matr[e1r][e2c]

    char2 = ''
    char2 = matr[e2r][e1c]

    return char1, char2

def encryptByPlayfairCipher(Matrix, plainList):
    CipherText = []
    for i in range(0, len(plainList)):
        c1 = 0
        c2 = 0
        ele1_x, ele1_y = search(Matrix, plainList[i][0])
        ele2_x, ele2_y = search(Matrix, plainList[i][1])

        if ele1_x == ele2_x:
            c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        elif ele1_y == ele2_y:
            c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_RectangleRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        cipher = c1 + c2
        CipherText.append(cipher)
    return CipherText


def removeSpaces_de(plain):
    # Remove all spaces in a string
    # Can be extended to remove punctuation
    return ''.join(plain.split())

def generateKeyTable_de(key):
    # Generates the 5x5 key square
    keyT = [['' for i in range(5)] for j in range(5)]
    dicty = {chr(i + 97): 0 for i in range(26)}

    for i in range(len(key)):
        if key[i] != 'j':
            dicty[key[i]] = 2
    dicty['j'] = 1

    i, j, k = 0, 0, 0
    while k < len(key):
        if dicty[key[k]] == 2:
            dicty[key[k]] -= 1
            keyT[i][j] = key[k]
            j += 1
            if j == 5:
                i += 1
                j = 0
        k += 1

    for k in dicty.keys():
        if dicty[k] == 0:
            keyT[i][j] = k
            j += 1
            if j == 5:
                i += 1
                j = 0

    return keyT

def search_de(keyT, a, b):
    # Search for the characters of a digraph in the key square and return their position
    arr = [0, 0, 0, 0]

    if a == 'j':
        a = 'i'
    elif b == 'j':
        b = 'i'

    for i in range(5):
        for j in range(5):
            if keyT[i][j] == a:
                arr[0], arr[1] = i, j
            elif keyT[i][j] == b:
                arr[2], arr[3] = i, j

    return arr

def mod5(a):
    # Function to find the modulus with 5
    if a < 0:
        a += 5
    return a % 5

def decrypt(str, keyT):
    # Function to decrypt
    ps = len(str)
    i = 0
    while i < ps:
        a = search_de(keyT, str[i], str[i+1])
        if a[0] == a[2]:
            str = str[:i] + keyT[a[0]][mod5(a[1]-1)] + keyT[a[0]][mod5(a[3]-1)] + str[i+2:]
        elif a[1] == a[3]:
            str = str[:i] + keyT[mod5(a[0]-1)][a[1]] + keyT[mod5(a[2]-1)][a[1]] + str[i+2:]
        else:
            str = str[:i] + keyT[a[0]][a[3]] + keyT[a[2]][a[1]] + str[i+2:]
        i += 2

    return str

def decryptByPlayfairCipher(str, key):
    # Function to call decrypt
    ks = len(key)
    key = removeSpaces_de(toLowerCase(key))
    str = removeSpaces_de(toLowerCase(str))
    keyT = generateKeyTable_de(key)
    return decrypt(str, keyT)


def main():
    st.title("Playfair Cipher Encryption/ Decryption")
    keyword = st.text_input("Enter Keyword:")
    menu_list = ["Encryption", "Decryption"]
    menu = st.radio("Menu", menu_list)  
    
    if (menu == 'Encryption'):
        plaintext = st.text_input("Enter Plain Text:")

        if keyword and plaintext:
            keyword = removeSpaces(toLowerCase(keyword))
            plaintext = removeSpaces(toLowerCase(plaintext))
            plaintextList = Diagraph(FillerLetter(plaintext))
            
            if len(plaintextList[-1]) != 2:
                plaintextList[-1] = plaintextList[-1] + 'z'
    
            Matrix = generateKeyTable(keyword, list1)
            cipherList = encryptByPlayfairCipher(Matrix, plaintextList)
    
            ciphertext = ""
            for i in cipherList:
                ciphertext += i
            
            st.subheader("Encrypted Text:")
            st.write(ciphertext)
            
        
            
    if (menu == 'Decryption'):
        ciphertext = st.text_input("Enter Ciphertext:")

        if keyword and ciphertext:
            keyword = removeSpaces_de(toLowerCase(keyword))
            ciphertext = removeSpaces_de(toLowerCase(ciphertext))
            plaintext = decryptByPlayfairCipher(ciphertext, keyword)

            st.subheader("Decrypted Text:")
            st.write(plaintext)

            

if __name__ == "__main__":
    main()
