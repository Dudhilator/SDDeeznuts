import pwinput
from datetime import datetime
from encryption import decrypt, encrypt
transactions = []

#Joshua did this bit 
def decrypt_database():  
    with open("usernamepassword.txt", "r") as f:
        return decrypt(f.read())

#print(decrypt_database()) #for debugging, note that the separator is !@#$%^&*()_+ and database in format of username!@#$%^&*()_+password!@#$%^&*()_+balance, with each line being a new entry

#Joshua copy pasted this from previous assignment
def verify_input(text, options): #this function just loops the input until the user inputs one of the options
    user_input = input(text).lower().strip()
    while user_input not in [option.lower() for option in options] or not user_input: # if user input is not exactly what is in options, or if input is empty string ask user to enter input again
        print("Invalid input, please try again.")
        user_input = input(text).lower().strip()
    return user_input 



#Both worked on this function
def login_menu():
    global current_balance, username, database, password, original_balance
    database = {}
    with open("usernamepassword.txt",'r') as f: 
        for line in decrypt_database().split(sep = "\n"): #split up the decrypted text into lines with each line being a different user
            database[line.strip().split(sep = "!@#$%^&*()_+")[0]] = (line.strip().split(sep = "!@#$%^&*()_+")[1], line.strip().split(sep = "!@#$%^&*()_+")[2]) # username: (password, balance)
    
    print('''Welcome to The Ryan Dunne Bank
-----------------------------------------------------------------------------------------------
INFORMATION 
We only accept positive whole numbers
Withdrawals have to be notes only
-----------------------------------------------------------------------------------------------
\n''')

    login_or_register = verify_input("Would you like to login or register? ", ["login", "register"])
    if login_or_register == "login": # if user logging in 
        logged_in = False 
        AmountOfTimesLoggedIn = 0 
        while not logged_in:
            username = input('Please enter your username: ')
            password = pwinput.pwinput('Please enter your password: ') #used pwinput instead of getpass because I wanted to see * instead of hiding the user input completely
            if username in database.keys(): #checks if the username is in the database 
                if database[username][0] == password: #if username in database, check if password is correct
                    current_balance = int(database[username][1])
                    original_balance = int(database[username][1])
                    print("Successfully logged in.")
                    logged_in = True 
                else:
                    print("Invalid username or password") 
                    AmountOfTimesLoggedIn += 1 
                    if AmountOfTimesLoggedIn == 3: #if they fail 3 times give option to go back so that they can register
                        print('It appears that you may have forgotten your credentials')
                        print('Would you like to keep trying or quit?')
                        print('1) Continue trying')
                        print('2) Quit')
                        action = verify_input('Press the number of the action you would like to do ',['1','2'])
                        match action:
                            case '1':
                                AmountOfTimesLoggedIn = 0
                            case '2':
                                print("\n")
                                login_menu()
            else: 
                print("Invalid username or password")
                AmountOfTimesLoggedIn += 1
                if AmountOfTimesLoggedIn == 3: #Samuel did the check for amount of times attempted
                    print('It appears that you have forgotten your credentials')
                    print('Would you like to keep trying or quit?')
                    print('1) Continue trying')
                    print('2) Quit')
                    action = verify_input('Press the number of the action you would like to do ',['1','2'])
                    match action:
                        case '1':
                            AmountOfTimesLoggedIn = 0
                        case '2':
                            login_menu()
    else: # if user registering
        is_registered = False #Joshua did the register thing 
        while not is_registered:
            username = input('What would you like your username to be? ') 
            password = pwinput.pwinput('What would you like your password to be? ') #use getpass to hide user password
            if username in database.keys(): #check if username taken  
                print("Username already taken, please enter another one")
            elif not username or not password: #if username and/or password is an empty string 
                print("Please enter a valid username or password")
            else: #valid registration 
                is_registered = True 
        data = decrypt_database() #have to save this to a variable before opening the file, because if i call it after opening the file, the file is wiped first and empty string is sent to decrypt/encrypt function causing the Fernet module to self destruct
        with open('usernamepassword.txt','w') as f:
            f.write(encrypt(data + f"\n{username}!@#$%^&*()_+{password}!@#$%^&*()_+0")) #add an extra line with new user, then encrypt and write it to the file 
        print("Successfully registered")
        current_balance = 0
        original_balance = 0
    main_menu()#once user been logged in or registered, start main program

#Both did this function
def main_menu(): 
    print("\n")
    print('What would you like to do?')
    print('1: Withdraw')
    print('2: Deposit')
    print('3: Check Balance')
    print('4: Quit')

    action = verify_input("Enter the number of the action you would like to do ", ["1","2","3","4", "withdraw", "deposit", "check balance", "balance", "quit"])
    match action:
        case "1": withdraw_function()
        case "2": deposit_function()
        case "3": balance_function()
        case "4": end_screen()
        case "withdraw": withdraw_function() #in case the user types the words instead
        case "deposit": deposit_function()
        case "check balance":balance_function()
        case "balance": balance_function()
        case "quit": end_screen()

#Samuel did this function
def find_largest_number(): #find how many digits each transaction has and return largest digit length
    global current_balance
    charactercountinglist = [len(str(transaction[1])) for transaction in transactions] #get the num of digit of each trarnsaction
    charactercountinglist.append(len(str(current_balance))) #add current balance
    charactercountinglist.sort(reverse = True)
    return charactercountinglist[0] #return the largest num of digit

#Samuel did this bit for formatting receipt 
def end_screen(): #print receipt
    global transactions, current_balance, original_balance
    if transactions: # if transactions took place 
        underscorecount = 0
        moniescount = 0
        balancecount = 0
        largest_number = find_largest_number()
        f = open('Receipt.txt','w')
        f.write('The Ryan Dunne Bank ATM Receipt\n')
        f.write('User: ' + username + "\n")

        while underscorecount <= largest_number+39: #fomrat the balance
            f.write('_')
            underscorecount += 1
        f.write('\n')
        f.write('\n')
        for monies in transactions:
            f.write(monies[2] + "   ")
            f.write(monies[0])
            monieslen = len(str(monies[1]))
            while moniescount <= largest_number-monieslen+7:
                f.write(' ')
                moniescount += 1
            f.write(str(monies[1]))
            f.write('\n')
            moniescount = 0
        f.write('\n')
        f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '   Balance   ') 
        balancelen = len(str(current_balance))
        underscorecount = 0
        while balancecount <= largest_number-balancelen+7:
            f.write(' ')
            balancecount += 1
        
        f.write(str(current_balance))
        f.write('\n')
        while underscorecount <= largest_number+39:
            f.write('_')
            underscorecount += 1
        f.write('\n')
        f.write('We strive to make the world')
        f.write('\n')
        f.write('a better place for the rich')
        f.close()
    else: # if no transactions take place 
        f = open('Receipt.txt','w')
        f.write('The Ryan Dunne Bank ATM Receipt\n')
        f.write('User: ' + username + "\n")
        f.write('______________________________________')
        f.write('\n')
        f.write('\n')
        f.write('No transactions took place')
        f.write('\n')
        f.write('\n')
        f.write('______________________________________')
        f.write('\n')
        f.write('We strive to make the world')
        f.write('\n')
        f.write('a better place for the rich')
        f.close()
    print('Thank you for using this Ryan Dunne bank ATM')

    #Joshua did the update to database section
    #write updatated balance into database
    database = decrypt_database().replace(f"{username}!@#$%^&*()_+{password}!@#$%^&*()_+{str(original_balance)}", f"{username}!@#$%^&*()_+{password}!@#$%^&*()_+{str(current_balance)}")#replace the old balance with the new balance 
    with open("usernamepassword.txt", "w") as f:
        f.write(encrypt(database)) #encrypt and write new balance to database
    
    #print(decrypt_database()) #for debugging

    quit()

#Both did this function 
def withdraw_function():
    global current_balance, username, password
    print('You have $'+str(current_balance) , 'in your account.')
    
    valid = False 
    while not valid: 
        withdraw_amount = input('How much would you like to withdraw? ')
        if not withdraw_amount.isdigit(): #check if all the characters are digits (3 in 1 check for string, floats and negatives) 
            print("Invalid input, please only enter a positive integer")
        elif int(withdraw_amount) % 5 != 0: #confirmed that it is an integer so can use the int() thing without an error 
            print('You can only withdraw money in $5, $10, $20, $50, and $100 notes. Please try again.')
        elif current_balance - int(withdraw_amount) < 0: #if attempting to withdraw more than they have
            print(f"You cannot withdraw more than in your balance. Your current balance is ${current_balance}. Please try again")
        else: #everything valid 
            withdraw_amount = int(withdraw_amount)#now that confirmed that user inputted an integer, can use int() function to convert to integer and not have an error
            valid = True 
    #Samuel did this bit
    final_balance = current_balance - withdraw_amount
    print('Successfully withdrawn ' + str(withdraw_amount) + '. You now have $' + str(final_balance) , 'in your account.')
    current_balance = int(final_balance) #update current balance, add the int() to copy the integer value 
    transactions.append(("Withdrawal", withdraw_amount, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))#add new transaction to list for the reciept

    main_menu()

#Both did this function
def deposit_function():
    global current_balance, username, password
    print('You have $'+str(current_balance) , 'in your account.')
    deposit_amount = input("How much would you like to deposit? ")
    while not deposit_amount.isdigit(): #check if the input has characters besides digits 
        print("Invalid input, please only enter a positive integer")
        deposit_amount = input("How much would you like to deposit? ")
    deposit_amount = int(deposit_amount) #now that confirmed that is integer, use int() function to convert to integer

    final_balance = current_balance + deposit_amount
    print("Successfully deposited " + str(deposit_amount) +'. You now have $' + str(final_balance) , 'in your account')
    current_balance = int(final_balance)
    transactions.append(("Deposit   ", deposit_amount, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))#add new transaction to list for the reciept
    main_menu()

#Samuel did this function
def balance_function():
    global current_balance
    print('You have $'+ str(current_balance) , 'in your account')
    main_menu()
    
if __name__ == "__main__": #Joshua did this 
    login_menu()