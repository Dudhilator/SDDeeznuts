import pwinput
transactions = []
def verify_input(text, options): #this function just loops the input until the user inputs one of the options
    user_input = input(text).lower().strip()
    while user_input not in [option.lower() for option in options] or not user_input: # if user input is not exactly what is in options, or if input is empty string ask user to enter input again
        print("Invalid input, please try again.")
        user_input = input(text).lower().strip()
    return user_input #copied from learning tool program 

def main_menu():
    global current_balance, username, database, password
    database = {}
    with open("usernamepassword.txt",'r') as f:
        for line in f.readlines():
            database[line.strip().split()[0]] = (line.strip().split()[1], line.strip().split()[2]) # username: (password, balance)
    
    print('Welcome to the Alexia T Martin Bank') 
    login_or_register = verify_input("Would you like to login or register? ", ["login", "register"])
    if login_or_register == "login": # if user logging in 
        logged_in = False 
        while not logged_in:
            username = input('Please enter your username: ')
            password = pwinput.pwinput('Please enter your password: ') #used pwinput instead of getpass because I wanted to see * instead of hiding the user input completely
            if username in database.keys(): #checks if the username is in the database 
                if database[username][0] == password: #if username in database, check if password is correct
                    current_balance = int(database[username][1])
                    print("Successfully logged in.")
                    logged_in = True 
                else:
                    print("Invalid username or password")#TODO add option to go back so you can register
            else:
                print("Invalid username or password")
    else: # if user registering 
        username = input('What would you like your username to be? ') 
        password = pwinput.pwinput('What would you like your password to be? ') #use getpass to hide user password
        while username in database.keys(): #check if username taken 
            print("Username already taken, please enter another one")
            username = input('What would you like your username to be? ') 
            password = pwinput.pwinput('What would you like your password to be? ')
        with open('usernamepassword.txt','a') as f:#TODO check for invalid character e.g. space as this could mess up database
            f.write(f"\n{username} {password} 0") #add user to database
        print("Successfully registered")
        current_balance = 0
    main()#once user been logged in or registered, start main program

def main():
    print("\n")
    print('What would you like to do?')
    print('1: Withdraw')
    print('2: Deposit')
    print('3: Check Balance')
    print('4: Quit')

    action = verify_input("Press the number of the action you would like to do ", ["1","2","3","4"])
    match action:
        case "1": withdraw_function()
        case "2": deposit_function()
        case "3": balance_function()
        case "4": end_screen()

def end_screen():#TODO finish receipt
    global transactions
    f = open('Receipt.txt','w')
    f.write('\n')
    f.close()
    print("Receipt.txt updated")
    print('Thank you for using this ATM bank ATM')
    print('\n')
    quit()

def withdraw_function():
    global current_balance, final_balance, username, password
    credentials = username + ' ' + password + ' ' + str(current_balance)
    print('You have $'+str(current_balance) , 'in your account.')

    withdraw_amount = int(input('How much would you like to withdraw? ')) #TODO check user input so that only integer
    if withdraw_amount % 5 != 0:
        print('You can only withdraw money in $5, $10, $20, $50, and $100 notes.')
        print('Would you like to try again?')
        try_again = verify_input("Yes or No? ", ["yes", "no"])
        if try_again.upper() == 'YES': withdraw_function()
        else: main()

    final_balance = current_balance - withdraw_amount
    final_credentials = username + ' ' + password + ' ' + str(final_balance)

    if final_balance >= 0:#check if amount withdrawn exceeds balance 
        with open('usernamepassword.txt',"r") as f:
            data = f.read()
            data = data.replace(credentials,final_credentials)
        with open("usernamepassword.txt", "w") as f:
            f.write(data) #write new balance to database
        print('Successfully withdrawn ' + str(withdraw_amount) + '. You now have $' + str(final_balance) , 'in your account.')
        current_balance = int(final_balance) #update current balance, add the int() to copy the integer value 
        transactions.append(("withdraw", current_balance, final_balance, withdraw_amount))#add new transaction to list for the reciept
    else:
        print('It appears you do not have this amount in your account.')
        print('Would you like to try again with a more suitable amount?')
        try_again = verify_input("Yes or No? ", ["yes", "no"])
        if try_again.upper() == 'YES': withdraw_function()
        else: main()
    main()

def deposit_function():
    print('deposit')
    global current_balance, final_balance, username, password
    credentials = username + ' ' + password + ' ' + str(current_balance)
    print('You have $'+str(current_balance) , 'in your account.')
    deposit_amount = input('How much would you like to deposit? ')
    final_balance = current_balance + int(deposit_amount)
    final_credentials = username + ' ' + password + ' ' + str(final_balance)
    
    with open('usernamepassword.txt', "r") as f:
        data = f.read()
        data = data.replace(credentials,final_credentials)
    with open("usernamepassword.txt", "w") as f:
        f.write(data)#write new balance to database

    print("Successfully withdrawn " + str(deposit_amount) +'. You now have $' + str(final_balance) , 'in your account')
    current_balance = int(final_balance)
    transactions.append(("deposit", current_balance, final_balance, deposit_amount))#add new transaction to list for the reciept
    main()

def balance_function():
    global current_balance
    print('You have $'+ str(current_balance) , 'in your account')
    main()

if __name__ == "__main__":
    main_menu()