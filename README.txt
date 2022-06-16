The Database in usernamepassword.txt is encrypted, if you want to see the database uncomment line 10 where it says print(decrypt_database())
Note that the separator is !@#$%^&*()_+ and each user is on a newline

You may need to reset usernamepassword.txt as the main program will self destruct if the key.txt and usernamepassword.txt is mismatched (error message: cryptography.fernet.InvalidToken)
to reset run the encryption.py file(which will update the key.txt file) and copy paste the encrypted text(first section) into the usernamepassword.txt and save it, then the main file should run properly
this wil ensure that the text in usernamepassword.txt is matched with the key in key.txt
this will reset the database to the 10 default users (10 because marking criteria said so) - "Includes 10 users with their: user login / PIN / balance / other data which may be relevant to the user"