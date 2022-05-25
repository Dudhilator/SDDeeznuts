yesnolist = ['YES' , 'NO']
def beginningmainmenuthing():
    global InitialBalance
    global username
    global password
    global validityvariable
    global usernamepassword
    validityvariable = 'F'
    f = open('usernamepassword.txt','r')
    print('Welcome to the Alexia T Martin Bank')
    username = input('Please enter your username ')
    password = input('Please enter your password ')
    for line in f.readlines():
        usernamepassword = line.split()
        if username == usernamepassword[0] and password == usernamepassword[1]:
            InitialBalance = int(usernamepassword[2])
            validityvariable = 'T'
    if validityvariable == 'F':
        print('This username and password have not been registered in our system')
        print('Would you like to register?')
        tryagain = input('Yes or No ')
        tryagainvariable = 'F'
        while tryagainvariable == 'F':
            if tryagain.upper() == 'YES':
                tryagainvariable = 'T' and registerfunction()
            if tryagain.upper() == 'NO':
                tryagainvariable = 'T' and endscreen()
            if tryagain.upper() not in yesnolist:
                print('Invalid input, please try again')
                tryagain = input('')
    f.close
def registerfunction():
    username = input('What would you like your username to be? ')
    password = input('What would you like your password to be? ')
    f = open('usernamepassword.txt','a')
    f.write(username)
    f.write(' ')
    f.write(password)
    f.write(' ')
    f.write('0')
    f.write('\n')
    f.close()
    print('Your new username is' , username , 'and your new password is' , password)
    print("Make sure you don't forget them")
    print('\n')
    beginningmainmenuthing()
def moneysectionfunction():
    global Withdrawvariable
    global Depositvariable
    global Balancevariable
    Withdrawvariable = 'F'
    Depositvariable = 'F'
    Balancevariable = 'F'
    whatiwanttodo = 'f'
    while whatiwanttodo == 'f':
        print('What would you like to do?')
        print('1: Withdraw')
        print('2: Deposit')
        print('3: Check Balance')
        print('4: Quit')
        whattheywanttodolol = input('')
        if whattheywanttodolol == '1':
            Withdrawvariable = 'T'
            whatiwanttodo = 't'
        if whattheywanttodolol == '2':
            Depositvariable = 'T'
            whatiwanttodo = 't'
        if whattheywanttodolol == '3':
            Balancevariable = 'T'
            whatiwanttodo = 't'
        if whattheywanttodolol == '4':
            endscreen()
        if whattheywanttodolol != '1' and whattheywanttodolol != '2' and whattheywanttodolol != '3':
            print('Put the right fucking thing in dumbass')
def endscreen():
    global usernamepassword
    f = open('Receipt.txt','w')
    f.write('\n')
    f.write(usernamepassword[2])
    print('Thank you for using this ATM bank ATM')
    print('\n')
    main()
def Withdrawfunction():
    global InitialBalance
    global Finalbalance
    global username
    global password
    credentials = username + ' ' + password + ' ' + str(InitialBalance)
    print('You have $'+str(InitialBalance) , 'in your account.')
    Withdrawalamount = int(input('How much would you like to withdraw? '))
    if Withdrawalamount%5 != 0:
        print('You can only withdraw money in $5, $10, $20, $50, and $100 notes.')
        print('Would you like to try again?')
        tryagain = input('Yes or no? ')
        tryagainvariable = 'F'
        while tryagainvariable == 'F':
            if tryagain.upper() == 'YES':
                tryagainvariable = 'T' and Withdrawfunction()
            if tryagain.upper() == 'NO':
                tryagainvariable = 'T' and mainpy()
            if tryagain.upper() not in yesnolist:
                print('Invalid input, please try again')
                tryagain = input('')
    Finalbalance = InitialBalance - Withdrawalamount
    finalcredentials = username + ' ' + password + ' ' + str(Finalbalance)
    if Finalbalance >= 0:
        with open('usernamepassword.txt','r') as f:
            data = f.read()
            data = data.replace(credentials,finalcredentials)
        with open('usernamepassword.txt','w') as f:
            f.write(data)
        print('You now have $' + str(Finalbalance) , 'in your account.')
    else:
        print('It appears you do not have this amount in your account.')
        print('Would you like to try again with a more suitable amount?')
        tryagain = input('Yes or No ')
        tryagainvariable = 'F'
        while tryagainvariable == 'F':
            if tryagain.upper() == 'YES':
                tryagainvariable = 'T' and Withdrawfunction()
            if tryagain.upper() == 'NO':
                tryagainvariable = 'T' and mainpy()
            if tryagain.upper() not in yesnolist:
                print('Invalid input, please try again')
                tryagain = input('')
    f = open('Receipt.txt','w')
    f.write(str(Withdrawalamount) + ' withdrawn')
    f.close()
def retryfunction():
    print('Would you like to make another transaction?')
    tryagain = input('Yes or No? ')
    tryagainvariable = 'F'
    while tryagainvariable == 'F':
        if tryagain.upper() == 'YES':
            tryagainvariable = 'T' and mainpy()
        if tryagain.upper() == 'NO':
            tryagainvariable = 'T' and endscreen()
        if tryagain.upper() not in yesnolist:
            print('Invalid input, please try again')
            tryagain = input('')
def Depositfunction():
    print('deposit')
    global InitialBalance
    global Finalbalance
    global username
    global password
    credentials = username + ' ' + password + ' ' + str(InitialBalance)
    print('You have $'+str(InitialBalance) , 'in your account.')
    Depositamount = input('How much would you like to deposit? ')
    Finalbalance = InitialBalance + int(Depositamount)
    finalcredentials = username + ' ' + password + ' ' + str(Finalbalance)
    with open('usernamepassword.txt','r') as f:
        data = f.read()
        data = data.replace(credentials,finalcredentials)
    with open('usernamepassword.txt','w') as f:
        f.write(data)
    print('You now have $' + str(Finalbalance) , 'in your account')
    f = open('Receipt.txt','w')
    f.write(Depositamount + ' deposited')
    f.close()
def Balancefunction():
    global InitialBalance
    print('Balancefunction')
    print('You have $'+ str(InitialBalance) , 'in your account')
def mainpy():
    moneysectionfunction()
    if Withdrawvariable =='T':
        Withdrawfunction()
    if Depositvariable == 'T':
        Depositfunction()
    if Balancevariable == 'T':
        Balancefunction()
    retryfunction()
def main():
    beginningmainmenuthing()
    mainpy()
main()

