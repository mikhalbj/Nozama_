import numpy as np
import csv
import random
import string
import uuid

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genUsers(n):

    firstNames = ['Alice', 'Brian', 'Carly', 'Dave', 'Luke', 'Mimi', 'Jack', 'Amelia', 'Alexandra']
    lastNames = ['King', 'McCarthy', 'Wang', 'O\'Halloran', 'Fedorov']
    seller = [True, False]
    users = []

    while len(users) < n:
        user = []
        index = uuid.uuid4()
        user.append(index)
        pw = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        f = firstNames[random.randint(0, 8)]
        l = lastNames[random.randint(0, 4)]
        user.append(genEmail(f, l))
        user.append(pw)
        user.append(f)
        user.append(l)
        user.append(genAddress())
        users.append(user)
    
    with open('data/Account.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, lineterminator='')
        for row in users:
            writer.writerow('\n')
            writer.writerow(row)
    
    genSeller(users)
    genBalance(users)
    return True


def genEmail(firstname, lastname):
    ends = ['@gmail.com', '@protonmail.com', '@duke.edu', '@unc.edu', '@ibm.com']
    misc = ['email', 'official', 'cvwhifbv', 'hello', 'personal']
    email = ''
    email += firstname
    email += lastname
    email += str(random.randint(0, 10000))
    email += misc[random.randint(0,4)]
    email += ends[random.randint(0,4)]
    return email


def genAddress():
    end = ['Rd.', 'St.', 'Ln.', 'Blvd.']
    num = ''.join(random.choice(string.digits) for _ in range(4))
    town = ['Durham NC', 'New York NY', 'Tuscaloosa TN', 'Fantasyland AB', 'Raleigh NC', 'Gotham NY']
    street = ['Main', 'Duke', 'Maple', 'MLK', 'Broadway', 'Mystery', 'South', 'US Highway 301']
    address = ''
    address = num + " " + random.choice(street) + " " + random.choice(end) + " " + random.choice(town)
    return address


def genSeller(users):
   # print("PRINTING USERS")
   # print(users)
    with open('data/Seller.csv', 'a', newline='') as sellfile:
        sellwriter = csv.writer(sellfile, lineterminator='')
        for row in users:
            if random.choices([True, False], weights=[0.3, 0.7]):
                sellwriter.writerow('\n')
                sellwriter.writerow([row[0]])
    return True


def genBalance(users):
    with open('data/Balance.csv', 'a', newline='') as bfile:
        bwriter = csv.writer(bfile, lineterminator='')
        for row in users:
            bwriter.writerow('\n')
            bwriter.writerow([row[0], round(random.uniform(0, 150), 2)])
    return True


if __name__ == "__main__":
    sizeOfUsers = 20
    genUsers(sizeOfUsers)
