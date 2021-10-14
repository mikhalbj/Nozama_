import numpy as np
import csv
import random
import string


def genUsers(n):

    with open('data/Account.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        lastrow = []
        for row in spamreader:
            lastrow = row
        print(lastrow)

    index = int(lastrow[0])
    firstNames = ['Alice', 'Brian', 'Carly', 'Dave', 'Luke', 'Mimi', 'Jack', 'Amelia', 'Alexandra']
    lastNames = ['King', 'McCarthy', 'Wang', 'O\'Halloran', 'Fedorov']
    seller = [True, False]
    users = []

    while len(users) < n:
        user = []
        index += 1
        user.append(index)
        pw = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        f = firstNames[random.randint(0, 8)]
        l = lastNames[random.randint(0, 4)]
        user.append(genEmail(f, l))
        user.append(pw)
        user.append(f)
        user.append(l)
        user.append(genAddress())
        print(user)
        users.append(user)
    
    with open('data/Account.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in users:
            writer.writerow(row)
    
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
    print(email)
    return email

def genAddress():
    end = ['Rd.', 'St.', 'Ln.', 'Blvd.']
    num = ''.join(random.choice(string.digits) for _ in range(4))
    town = ['Durham NC', 'New York NY', 'Tuscaloosa TN', 'Fantasyland AB', 'Raleigh NC', 'Gotham NY']
    street = ['Main', 'Duke', 'Maple', 'MLK', 'Broadway', 'Mystery', 'South', 'US Highway 301']
    address = ''
    address = num + " " + random.choice(street) + " " + random.choice(end) + " " + random.choice(town)
    return address

if __name__ == "__main__":
    sizeOfUsers = 20
    genUsers(sizeOfUsers)
