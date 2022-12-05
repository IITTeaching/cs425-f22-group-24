# Group 24 Banking Application implementation
# Shambhawi Sharma, Brenda Coronel, Syed Rahman, Rohit Pemmasani

import psycopg2
import uuid
from os import system

conn = psycopg2.connect(
    host="localhost",
    database="Banking_Application",
    user="postgres",
    password="Supriya.2402"
)

conn.autocommit = True
cursor=conn.cursor()

aid = 10000000
account_type = {0:"SAVING", 1:"CHECKING"}
transaction_type = {0:"Deposit Amount", 1:"Withdraw Amount", 2:"Transfer" }

# function to transfer money across accounts
def transfer(customerId):
    cursor.execute(f"select * from accounts where customer_id = '{customerId}';")
    userAccounts = cursor.fetchall()
    print("Accounts:\n")
    userAccountsDict ={}
    for i in range(len(userAccounts)):
        userAccountsDict[int(i)] = userAccounts[i][0]
        print(f"{i}: Id -> {userAccounts[i][0]} Account Type -> {userAccounts[i][1]} Balance-> {userAccounts[i][2]} \n")
    accountChoiceID = int(input("Please select account for withdrawal :"))
    transferAccountID = input("Please enter the Account ID to you want to transfer :")
    amount = float(input("Please enter the amount you want to transfer : "))
    cursor.execute(f"select * from accounts where account_id = '{userAccountsDict[accountChoiceID]}';")
    rec = cursor.fetchall()
    print(f"Current Balance Before Transfer : {rec[0][2]}")
    accountBalance = rec[0][2] - amount
    cursor.execute(f"update accounts set balance = {accountBalance} where account_id = '{userAccountsDict[accountChoiceID]}';")
    cursor.execute(f"select * from accounts where account_id = '{transferAccountID}';")
    rec2 = cursor.fetchall()
    print(f"Current Balance Before Transfer : {rec2[0][2]}")
    accountBalance = rec2[0][2] + amount
    cursor.execute(f"update accounts set balance = {accountBalance} where account_id = '{transferAccountID}';")
    print("Transaction Successfull!")
    cursor.execute(f"insert into transaction values('{transferAccountID}', '{userAccountsDict[accountChoiceID]}', 'Transfer', {amount}, 'Debit Cash from former, Credit Cash from latter', current_timestamp);")

# function to create new account
def createAccount(customerId):
    cursor.execute("select * from branches")
    branch_dict = {}
    rec = cursor.fetchall()
    print("Select branch\n")
    for branch in rec:
        branch_dict[branch[1]] = branch[0]
        print(f"id:{branch[1]} address:{branch[0]}")
    b_id = int(input("Enter branch id\n"))
    print("Select account type")
    for i in range(len(account_type)):
        print(f"{i}: {account_type[i]}")
    a_type = int(input("Enter account type\n"))
    balance = float(input("Enter balance\n"))
    cursor.execute(f"insert into accounts values('{str(uuid.uuid4())}', '{account_type[a_type]}', '{balance}', '{customerId}', '{branch_dict[b_id]}');")

# function to withdraw money from account
def withdraw(customerId):
    cursor.execute(f"select * from accounts where customer_id = '{customerId}';")
    userAccounts = cursor.fetchall()
    print("Accounts:\n")
    userAccountsDict ={}
    for i in range(len(userAccounts)):
        userAccountsDict[int(i)] = userAccounts[i][0]
        print(f"{i}: Id -> {userAccounts[i][0]} Account Type -> {userAccounts[i][1]} Balance-> {userAccounts[i][2]} \n")
    accountChoiceID = int(input("Please select account for withdrawal :"))
    amount = float(input("Please enter the amount you want to withdraw : "))
    cursor.execute(f"select * from accounts where account_id = '{userAccountsDict[accountChoiceID]}';")
    rec = cursor.fetchall()
    accountBalance = rec[0][2] - amount
    if accountBalance < 0:
        print("Cant perform this operation")
        print("Please try again with lesser amount")
        printCustomerOpertaionPage(customerId)
    else:
        cursor.execute(f"update accounts set balance = {accountBalance} where account_id = '{userAccountsDict[accountChoiceID]}';")
        print("Transaction Successfull")
        print(f"Current Balance : {accountBalance}")
        cursor.execute(f"insert into transaction values('Self', '{rec[0][0]}', 'Withdrawal', {amount}, 'Credit Cash', current_timestamp);")
    
# function to deposit money to account
def deposit(customerId):
    cursor.execute(f"select * from accounts where customer_id = '{customerId}';")
    userAccounts = cursor.fetchall()
    print("Accounts:\n")
    userAccountsDict ={}
    for i in range(len(userAccounts)):
        userAccountsDict[int(i)] = userAccounts[i][0]
        print(f"{i}: Id -> {userAccounts[i][0]} Account Type -> {userAccounts[i][1]} Balance-> {userAccounts[i][2]} \n")
    accountChoiceID = int(input("Please select account for deposit :"))
    amount = float(input("Please enter the amount you want to deposit : "))
    cursor.execute(f"select * from accounts where account_id = '{userAccountsDict[accountChoiceID]}';")
    rec = cursor.fetchall()
    print(f"Current Balance : {rec[0][2]}")
    accountBalance = rec[0][2] + amount
    cursor.execute(f"update accounts set balance = {accountBalance} where account_id = '{userAccountsDict[accountChoiceID]}';")
    print("Transaction Successfull")
    print(f"Current Balance : {accountBalance}")
    cursor.execute(f"insert into transaction values('{rec[0][0]}', 'Self', 'Deposit', {amount}, 'Debit Cash', current_timestamp);")

# function to print welcome page and login page
def printLoginOperations():
    print("Welcome to just your generic bank ☆*: .｡. o(≧▽≦)o .｡.:*☆")
    print("Please select your login type from the following:")
    print("1 : Customer")
    print("2 : Manager")
    print("3 : Teller")
    print("To exit, press 4")

# function to print Customer Operations page
def printCustomerOpertaionPage(customerId):
    _ = system('cls')
    print("Operation that customer can perform goes here!")
    print("1: Deposit to Account")
    print("2: Withdraw from Account")
    print("3: Transfer to Account")
    print("4: Logout")
    accountOperationChoice = int(input("Enter you choice : "))
    if accountOperationChoice == 1:
        deposit(customerId)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            printCustomerOpertaionPage(customerId)

    elif accountOperationChoice == 2:
        withdraw(customerId)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            printCustomerOpertaionPage(customerId)
    
    elif accountOperationChoice == 3:
        transfer(customerId)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            printCustomerOpertaionPage(customerId)

    else:
        _ = system('cls')
        interface()

# function to print Manager Operations page
def managerOperations(employeeId):
    _ = system('cls')
    print("Operation that manager can perform goes here!")
    print("1: Deposit to Account")
    print("2: Withdraw from Account")
    print("3: Transfer to Account")
    print("4: View Customer Info")
    print("5: View Total Branch Balance and Transactions By Today")
    print("6: Logout")
    choice = int(input("Enter your choice : "))
    if choice == 1:
        cid = input("Please enter a valid customer id : ")
        deposit(cid)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            managerOperations(employeeId)

    elif choice == 2:
        cid = input("Please enter a valid customer id : ")
        withdraw(cid)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            managerOperations(employeeId)

    elif choice == 3:
        cid = input("Please enter a valid customer id : ")
        transfer(cid)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            managerOperations(employeeId)

    elif choice == 4:
        cursor.execute(f"select * from customers where branch_addr = (select branch_addr from employees where ssn = '{employeeId}');")
        rec = cursor.fetchall()
        for i in range(len(rec)):
            print(f"Customer Id -> {rec[i][0]}, Customer Name -> {rec[i][1]}, Customer Address -> {rec[i][2]}, Branch Address -> {rec[i][3]}\n")
        cursor.execute(f"select count(customer_id) from customers where branch_addr = (select branch_addr from employees where ssn = '{employeeId}');")
        total_customers = cursor.fetchall()
        print(f"Total number of customers -> {total_customers[0][0]}\n")
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            managerOperations(employeeId)

    elif choice == 5:
        cursor.execute(f"select sum(balance) from accounts where branch_addr = (select branch_addr from employees where ssn = '{employeeId}');")
        rec = cursor.fetchall()
        print(f"Total balance in branch -> {rec[0][0]}\n")
        cursor.execute(f"select current_timestamp;")
        current_time = cursor.fetchall()
        cursor.execute(f"select * from transaction where time < '{current_time[0][0]}'")
        rec = cursor.fetchall()
        for i in range(len(rec)):
            print(f"To Account Id -> {rec[i][0]} ||||| From Account Id -> {rec[i][1]} ||||| Type of Transaction -> {rec[i][2]} ||||| Amount -> {rec[i][3]} ||||| Description -> {rec[i][4]} ||||| Time -> {rec[i][5]}\n")
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            managerOperations(employeeId)

    else:
        _ = system('cls')
        interface()

# function to print Teller Operations page
def tellerOperations():
    _ = system('cls')
    print("Operation that teller can perform goes here!")
    print("1: Deposit to Account")
    print("2: Withdraw from Account")
    print("3: Transfer to Account")
    print("4: Logout")
    choice = int(input("Enter your choice : "))
    if choice == 1:
        cid = input("Please enter a valid customer id : ")
        deposit(cid)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            tellerOperations()

    elif choice == 2:
        cid = input("Please enter a valid customer id : ")
        withdraw(cid)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            tellerOperations()

    elif choice == 3:
        cid = input("Please enter a valid customer id : ")
        transfer(cid)
        print("Press y to continue ....")
        userContinue = input("")
        if userContinue == 'y':
            tellerOperations()

    else:
        _ = system('cls')
        interface()

# function to start app and navigate between customer, manager and teller logins
def interface():
    choice = None
    printLoginOperations()
    choice = int(input(" Enter you choice :  "))
    print("\n")
    if choice == 1:
        customerId = input("Please enter your customer-ID: ")
        customerPass = input("Please enter your password : ")
        cursor.execute(f"select * from customers where customer_id = '{customerId}' and password = '{customerPass}';")
        rec = cursor.fetchall()
        if rec :
            _ = system('cls')
            print("Logged in successfully!")
            printCustomerOpertaionPage(customerId)
           
        else:
            _ = system('cls')
            print("Invalid Credentials\n")
            print("Please try again ")
            interface()
            
    elif choice == 2:
        # login in manager
        employeeId = input("Please enter your Employee-ID: ")
        cursor.execute(f"select * from employees where ssn = {employeeId} and role_emp='manager';")
        rec = cursor.fetchall()
        if rec :
            _ = system('cls')
            print("Logged in successfully!")
            managerOperations(employeeId)
        else:
            _ = system('cls')
            print("Invalid Credentials\n")
            print("Please try again ")
            interface()

    elif choice == 3:
        # login in Teller
        employeeId = input("Please enter your Employee-ID: ")
        cursor.execute(f"select * from employees where ssn = {employeeId} and role_emp='teller';")
        rec = cursor.fetchall()
        if rec :
            _ = system('cls')
            print("Logged in successfully!")
            tellerOperations()
        else:
            _ = system('cls')
            print("Invalid Credentials\n")
            print("Please try again ")
            interface()
    
    else:
        quit

interface()