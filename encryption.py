import random 
from cryptography.fernet import Fernet
#key.txt has 5 lines, first line is key for caesar cipher, second is for key cipher, third is for Fernet module, fourth is whether to add or subtract for key_encrypt/decrypt, fifth is whether to add or subtract for caesar_encrypt/decrypt

#both did encrypt and decrypt
def encrypt(text):
    return caesar_encrypt(key_encrypt(fernet_encrypt(text))) #encrypt the line 3 times and return encrypted text 

def decrypt(text):
    return fernet_decrypt(key_decrypt(caesar_decrypt(text))) #decrypt in opposite order and return decrypted text


#Joshua did read_key and write_key
def read_key(line_num): #read key at line number
    with open("key.txt", "r") as f:
        return f.readlines()[line_num].strip()

def write_key(key, line_num): #write the key to the line number needed 
    with open("key.txt", "r") as f: #for some reason r+ does some wacky stuff so have to manually open to read then close then open to write 
        content = f.readlines()
    content[line_num] = key if line_num == 4 else key + "\n" #change the line to new key
    with open("key.txt","w") as f:
        f.writelines(content)


#Samuel did caesar_encrypt/decrypt
def caesar_encrypt(text): # for each character in the text, convert to unicode add a random amount and convert back to character
    key = random.randint(-10, 10)#generate a random number
    write_key(str(key), 0)#write the key on the first line of the key.txt file
    result = ''#empty string :)
    caesarlist = []#empty list :O
    for char in text:#for each character in the text
        if ord(char) >= 100:#if the unicode of the character is bigger than 99 then we need to subtract the key
            if key >= 0:#if the key is a positive number then we can just subtract normally
                finnishchar = chr(ord(char)-key)
                caesarlist.append('P')
            if key < 0:#if the key is a negative number, then just adding would be subtracting
                finnishchar = chr(ord(char)+key)
                caesarlist.append('S')
        if ord(char) < 100:#if the unicode of the character is smaller than 100, then adding the key is fine and will be within the character map
            finnishchar = chr(ord(char)+key)
            caesarlist.append('S')
        result += finnishchar#add the shifted character to the empty string
    write_key(''.join(caesarlist), 4)#write the p's and the s's in the 5th line of the key.txt file for decryption
    return result 


def caesar_decrypt(text):
    key = read_key(0)#read the key that was used to encrypt
    caesarlist = read_key(4)#read the series of p's and s's which tells us whether to add or subtract
    unencryptedlist = ''#another empty list
    for charnumber in range(len(text)):#give each character in the input text a number
        caesarnumber = caesarlist[charnumber]#find whether the character corresponds with a p or an s
        if caesarnumber == 'P':
            finnishchar = chr(ord(text[charnumber])+int(key))#if it is a p, then we add the key to decrypt
        if caesarnumber == 'S':
            finnishchar = chr(ord(text[charnumber])-int(key))#if it is an s, then we subtract the key to decrypt
        unencryptedlist += finnishchar#add the decrypted characters to the empty string.
    return unencryptedlist


#Samuel did key_encrypt/decrypt
def key_encrypt(text):
    result = ''#ANOTHER ONE
    keything = [random.randint(1,9) for _ in range(len(text))] #get a random int from 1 - 9 for every character in usernamepassword.txt
    keylist = []#empty list
    for i in range(len(text)):#each character in the input text has a corresponding key which is in 'keything'
        if ord(text[i]) >= 100:#if the unicode of the character is greater than 99, minus the corresponding key.
            finnishchar = chr(ord(text[i]) - keything[i])
            keylist.append('P')#if we subtracted the key, append a 'p'. this is similar to the caesar cipher but it was 'p' and 's' before.
        else:#if the unicode of the character is not greatter than 99, add the corresponding key
            finnishchar = chr(ord(text[i]) + keything[i])
            keylist.append('O')#if we added the key, append an 'o'
        result += finnishchar #add the encrypted characters to the empty string.
    write_key(''.join(keylist),3)#write the keylist in the 4th line of the key.txt file for decryption
    final_key = ''.join([str(a) for a in keything]) #convert all the int in the list into string and join together 
    write_key(str(final_key), 1)#write the key into the text file so that can use it for decrypt 
    return result 

def key_decrypt(text):
    keylist = read_key(3)#read the key from the txt.file.
    unencryptedlist = ''#EMPTY STRING WOO
    keything = [int(char) for char in read_key(1)] #convert the keything to list of integers
    for charnumber in range(len(text)):#each character in the input text is given a number which allows us to find the corresponding key.
        keynumber = keylist[charnumber]#the letter of 'p' or 'o' which corresponds to the character is called keynumber
        if keynumber == 'P':#if corresponding letter is 'p' then we add the key
            finnishchar = chr(ord(text[charnumber])+keything[charnumber])
        if keynumber == 'O':#if corresponding letter is 'o' then we subtract the key
            finnishchar = chr(ord(text[charnumber])-keything[charnumber])
        unencryptedlist += finnishchar #add the decrypted text to the empty string
    return unencryptedlist

#Joshua did fernet_encrypt/decrypt
#this bit mega annoying since had to keep converting to string to write/read to file then to byte to encrypt/decrypt
def fernet_encrypt(text):
    key = Fernet.generate_key() #make a new key (in byte)
    write_key(key.decode("utf-8"), 2) #convert to string and write to file 
    key_object = Fernet(key) #use the byte to make a fernet key object 
    return key_object.encrypt(bytes(text, 'utf-8')).decode("utf-8") #turn the text into a byte so that the key object can encrypt, then turn back into string 

def fernet_decrypt(text):
    key_object = Fernet(bytes(read_key(2), "utf-8")) #read the key and turn into byte, then turn into key object
    return key_object.decrypt(bytes(text,"utf-8")).decode('utf-8') #turn the text into bytes for the key object to decrypt, then turn back into string 


#Joshua did the reset database thing
if __name__ == "__main__": #this part only runs if you manually run this file, and does not run when imported in ATM.py
    a = encrypt("Dunne!@#$%^&*()_+1111!@#$%^&*()_+1000\nRyan!@#$%^&*()_+1234!@#$%^&*()_+0\nRyan_Dunne!@#$%^&*()_+12345!@#$%^&*()_+9999999999999999\nMr_Dunne!@#$%^&*()_+asdf!@#$%^&*()_+1\nRyan Dunne Sr.!@#$%^&*()_+asdfghjkl!@#$%^&*()_+42069\nMlexia T Aartin!@#$%^&*()_+tiFCw_FrP0iY1kvd-R7WZeCfDDdpnrUwQtX0ygzAv3I=!@#$%^&*()_+1234567890\nXx_RyanDunne69420_xX!@#$%^&*()_+password!@#$%^&*()_+987654321\nR.Dunne!@#$%^&*()_+qwertyuiop!@#$%^&*()_+0\n          ryan              dunne           !@#$%^&*()_+      p a s s w o r d          !@#$%^&*()_+21\ndunner!@#$%^&*()_+*****!@#$%^&*()_+4")
    print(a)
    print("\n")
    print(decrypt(a)) #testing if encrypt and decrypt both work
    
    #The above is template in case need to reset usernamepassword.txt as the key is changed each time you use the encrypt function, as main program cooks if usernamepassword.txt is empty 
    #It will reset the database to the default 10 users (need 10 users because the marking criteria said so)
    #run this file and copy paste the encrypted text(first line) into the usernamepassword.txt and save it, then the main file should run properly

