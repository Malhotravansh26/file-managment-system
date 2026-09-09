import string
import random
import json
from pathlib import Path


class Bank:
    database = Path(__file__).parent / 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())

        else:
            print("no such file exist")

    except Exception as err:
        print(f"error accord due to {err}")

    @classmethod
    def __updatedata(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __generateAcc(cls):
        while True:
            alpha = random.choices(string.ascii_letters, k=4)
            digits = random.choices(string.digits, k=3)
            schar = random.choices("!@#$%^&*", k=3)

            id = alpha + digits + schar
            random.shuffle(id)

            acc = "".join(id)

            if not any(i.get("AccountNo.") == acc for i in Bank.data):
                return acc

    def create_account(self):
        try:
            info = {
                "Name": input("Enter your name :- "),
                "Age": int(input("Enter your age here :- ")),
                "Email": input("Enter your email address :- "),
                "Pin": int(input("Enter your 4 digit account pin :- ")),
                "AccountNo.": Bank.__generateAcc(),
                "Balance": 0
            }
        except ValueError:
            print("Please enter valid numeric values for age and PIN.")
            return

        if info['Age'] < 18 or len(str(info['Pin'])) != 4:
            print("Error occurred in opening of account")
            return

        print("YOUR ACCOUNT OPEN IN OUR ACCOUNT SUCCESSFULLY")

        for i in info:
            print(f"{i} : {info[i]}")

        print("Please note down your account number")

        Bank.data.append(info)

        Bank.__updatedata()

    def deposit_money(self):
        accountno = input("Enter your account number: ")

        try:
            pin = int(input("Enter your pin: "))
        except ValueError:
            print("Invalid PIN")
            return

        userdata = [
            i for i in Bank.data
            if i['AccountNo.'] == accountno and i['Pin'] == pin
        ]

        if not userdata:
            print("Sorry, user not found")
            return

        try:
            amount = int(input("Enter amount of deposit money :- "))
        except ValueError:
            print("Please enter a valid amount")
            return

        if amount > 10000 or amount <= 0:
            print("Transaction limit exceeded")
        else:
            userdata[0]['Balance'] += amount

            Bank.__updatedata()
            print("YOUR AMOUNT DEPOSITED SUCCESSFULLY")

    def withdraw_money(self):
        accountno = input("Enter your account number: ")

        try:
            pin = int(input("Enter your pin: "))
        except ValueError:
            print("Invalid PIN")
            return

        userdata = [
            i for i in Bank.data
            if i['AccountNo.'] == accountno and i['Pin'] == pin
        ]

        if not userdata:
            print("Sorry, user not found")
            return

        try:
            amount = int(input("Enter amount of withdraw money :- "))
        except ValueError:
            print("Please enter a valid amount")
            return

        if amount <= 0:
            print("Amount must be greater than 0")

        elif amount > 10000:
            print("Maximum withdrawal limit is 10000")

        elif userdata[0]['Balance'] < amount:
            print("You don't have enough money")

        else:
            userdata[0]['Balance'] -= amount

            print("YOUR AMOUNT WITHDRAWN SUCCESSFULLY")
            Bank.__updatedata()

    def check_details(self):
        accnumber = input("Please tell your account number: ")

        try:
            pin = int(input("Please tell your pin as well: "))
        except ValueError:
            print("Invalid PIN")
            return

        userdata = [
            i for i in Bank.data
            if i['AccountNo.'] == accnumber and i['Pin'] == pin
        ]

        if not userdata:
            print("User not found")
            return

        print("Your information are\n")

        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")

    def update_details(self):
        accnumber = input("Please tell your account number: ")

        try:
            pin = int(input("Please tell your pin as well: "))
        except ValueError:
            print("Invalid PIN")
            return

        userdata = [
            i for i in Bank.data
            if i['AccountNo.'] == accnumber and i['Pin'] == pin
        ]

        if not userdata:
            print("User not found")
            return

        print("You cannot update balance, account number and age")
        print("Enter your new details and if not then simply skip it")

        new_name = input(
            "Enter your updating name or just skip it: "
        )

        new_email = input(
            "Enter your updating email or just skip it: "
        )

        new_pin = input(
            "Enter your new pin or just skip it: "
        )

        if new_name == "":
            new_name = userdata[0]["Name"]

        if new_email == "":
            new_email = userdata[0]["Email"]

        if new_pin == "":
            new_pin = userdata[0]["Pin"]

        elif not new_pin.isdigit() or len(new_pin) != 4:
            print("PIN must contain exactly 4 digits")
            return

        else:
            new_pin = int(new_pin)

        newdata = {
            "Name": new_name,
            "Email": new_email,
            "Pin": new_pin,
            "Age": userdata[0]['Age'],
            "AccountNo.": userdata[0]['AccountNo.'],
            "Balance": userdata[0]['Balance']
        }

        for i in newdata:
            if newdata[i] == userdata[0][i]:
                continue
            else:
                userdata[0][i] = newdata[i]

        Bank.__updatedata()

        print("YOUR DETAILS UPDATED SUCCESSFULLY")

    def delete_account(self):
        accnumber = input("Please tell your account number: ")

        try:
            pin = int(input("Please tell your pin as well: "))
        except ValueError:
            print("Invalid PIN")
            return

        userdata = [
            i for i in Bank.data
            if i['AccountNo.'] == accnumber and i['Pin'] == pin
        ]

        if not userdata:
            print("User not found")
            return

        check = input(
            "Press y for yes and n for no to delete account: "
        )

        if check == 'n' or check == 'N':
            print("Delete operation cancelled")
            return

        elif check != 'y' and check != 'Y':
            print("Invalid choice")
            return

        index = Bank.data.index(userdata[0])

        Bank.data.pop(index)

        print("Your bank account deleted successfully")

        Bank.__updatedata()


print("Press 1 for creating a new bank account")
print("Press 2 for depositing money in your account")
print("Press 3 for withdrawing money from your account")
print("Press 4 for checking your account balance")
print("Press 5 for updating details of your account")
print("Press 6 for deleting your account")

try:
    res = int(input("Enter your choice: "))
except ValueError:
    print("Please enter a valid choice")
    exit()

user = Bank()

if res == 1:
    user.create_account()

if res == 2:
    user.deposit_money()

if res == 3:
    user.withdraw_money()

if res == 4:
    user.check_details()

if res == 5:
    user.update_details()

if res == 6:
    user.delete_account()