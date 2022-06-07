import random 
from cryptography.fernet import Fernet
#key.txt has 3 lines, first line is key for caesar cipher, second is for key cipher and third is for Fernet module

def encrypt(text):
    return caesar_encrypt(key_encrypt(fernet_encrypt(text))) #encrypt the line 3 times and return encrypted text 

def decrypt(text):
    return fernet_decrypt(key_decrypt(caesar_decrypt(text))) #decrypt in opposite order and return decrypted text



def read_key(line_num): #read key at line number
    with open("key.txt", "r") as f:
        return f.readlines()[line_num].strip()

def write_key(key, line_num): #write the key to the line number needed 
    with open("key.txt", "r") as f: #for some reason r+ does some wacky stuff so have to manually open to read then close then open to write 
        content = f.readlines()
    content[line_num] = key + "\n"
    with open("key.txt","w") as f:
        f.writelines(content)



def caesar_encrypt(text):
    key = random.randint(-10, 10)
    write_key(str(key), 0)
    result = ''
    caesarlist = []
    for char in text:
        if ord(char) >= 100:
            if key >= 0:
                finnishchar = chr(ord(char)-key)
                caesarlist.append('P')
            if key < 0:
                finnishchar = chr(ord(char)+key)
                caesarlist.append('S')
        if ord(char) < 100:
            finnishchar = chr(ord(char)+key)
            caesarlist.append('S')
        result += finnishchar
    write_key(''.join(caesarlist), 5)
    return result # for each character in the text, convert to unicode add 2 and convert back to character


def caesar_decrypt(text):
    key = read_key(0)
    caesarlist = read_key(5)
    unencryptedlist = ''
    for charnumber in range(len(text)):
        caesarnumber = caesarlist[charnumber]
        if caesarnumber == 'P':
            finnishchar = chr(ord(text[charnumber])+int(key))
        if caesarnumber == 'S':
            finnishchar = chr(ord(text[charnumber])-int(key))
        unencryptedlist += finnishchar
    return unencryptedlist #same as encrypt but backwards 



def key_encrypt(text):
    result = ''
    keything = [random.randint(1,9) for _ in range(len(text))] #get a random int from 1 - 3 for every character in usernamepassword.txt
    keylist = []
    for i in range(len(text)):
        if ord(text[i]) >= 100:
            finnishchar = chr(ord(text[i]) - keything[i])
            keylist.append('P')
        else:
            finnishchar = chr(ord(text[i]) + keything[i])
            keylist.append('O')
        result += finnishchar #change the character at that index into unicode then adds corresponding number in keything, then converts back into character
    write_key(''.join(keylist),4)
    final_key = ''.join([str(a) for a in keything]) #convert all the int in the list into string and join together 
    write_key(str(final_key), 1)#write the key into the text file so that can use it for decrypt 
    return result 

def key_decrypt(text):
    keylist = read_key(4)
    unencryptedlist = ''
    keything = [int(char) for char in read_key(1)] #convert the keything to list of integers
    for charnumber in range(len(text)):
        keynumber = keylist[charnumber]
        if keynumber == 'P':
            finnishchar = chr(ord(text[charnumber])+keything[charnumber])
        if keynumber == 'O':
            finnishchar = chr(ord(text[charnumber])-keything[charnumber])
        unencryptedlist += finnishchar #subtract the corresponding num in the keylist from each character in the string
    return unencryptedlist


#this bit mega annoying since had to keep converting to string to write/read to file then to byte to encrypt/decrypt
def fernet_encrypt(text):
    key = Fernet.generate_key() #make a new key (in byte)
    write_key(key.decode("utf-8"), 2) #convert to string and write to file 
    key_object = Fernet(key) #use the byte to make a fernet key object 
    return key_object.encrypt(bytes(text, 'utf-8')).decode("utf-8") #turn the text into a byte so that the key object can encrypt, then turn back into string 

def fernet_decrypt(text):
    key_object = Fernet(bytes(read_key(2), "utf-8")) #read the key and turn into byte, then turn into key object
    return key_object.decrypt(bytes(text,"utf-8")).decode('utf-8') #turn the text into bytes for the key object to decrypt, then turn back into string 