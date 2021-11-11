import numpy as np
import csv
import random
import string
import uuid

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genUsers(n):

    firstNames = ['Alice', 'Brian', 'Carly', 'Dave', 'Luke', 'Mimi', 'Jack', 'Amelia', 'Alexandra', 'Julie', 'Martha', 'Frank', 'Yoko', 'Mark']
    lastNames = ['King', 'McCarthy', 'Wang', 'O\'Halloran', 'Fedorov', 'Holzer', 'Price', 'Chodri', 'Ogawa', 'Fisher', 'Rhys', 'Sontag', 'Odell']
    seller = [True, False]
    users = []

    while len(users) < n:
        user = []
        index = uuid.uuid4()
        user.append(index)
        pw = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        f = firstNames[random.randint(0, len(firstNames)-1)]
        l = lastNames[random.randint(0, len(lastNames)-1)]
        user.append(genEmail(f, l))
        user.append(pw)
        user.append(f)
        user.append(l)
        user.append(genAddress())
        users.append(user)
    
    with open('data/Account.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='unix')
        for row in users:
            writer.writerow(row)
    
    genSeller(users)
    genBalance(users)
    return True


def genEmail(firstname, lastname):
    ends = ['@gmail.com', '@protonmail.com', '@duke.edu', '@unc.edu', '@ibm.com', '@email.com', '@aol.com', '@fake.edu']
    misc = ['email', 'official', 'cvwhifbv', 'hello', 'personal', '12345', '67890', 'mailaddress', 'whocaresemail']
    email = ''
    email += firstname
    email += lastname
    email += str(random.randint(0, 10000))
    email += misc[random.randint(0,len(misc)-1)]
    email += ends[random.randint(0,len(ends)-1)]
    return email


def genAddress():
    end = ['Rd.', 'St.', 'Ln.', 'Blvd.', 'Dr.', 'Avn', 'Circle', 'Crt.']
    num = ''.join(random.choice(string.digits) for _ in range(4))
    town = ['Durham NC', 'New York NY', 'Tuscaloosa TN', 'Fantasyland AB', 'Raleigh NC', 'Gotham NY', 'Asheboro NC', 'Austin TX', 'Paris TX']
    street = ['Main', 'Duke', 'Maple', 'MLK', 'Broadway', 'Mystery', 'South', 'US Highway 301', 'Broad', 'Trinity', 'Memorial', 'Business']
    address = ''
    address = num + " " + random.choice(street) + " " + random.choice(end) + " " + random.choice(town)
    return address


def genSeller(users):
   # print("PRINTING USERS")
   # print(users)
    with open('data/Seller.csv', 'w') as sellfile:
        sellwriter = csv.writer(sellfile, dialect='unix')
        for row in users:
            if random.choices([True, False], weights=[0.3, 0.7]):
                sellwriter.writerow([row[0]])
    return True


def genBalance(users):
    with open('data/Balance.csv', 'w') as bfile:
        bwriter = csv.writer(bfile, dialect='unix')
        for row in users:
            bwriter.writerow([row[0], round(random.uniform(0, 150), 2)])
    return True


if __name__ == "__main__":
    sizeOfUsers = 20
    genUsers(sizeOfUsers)
