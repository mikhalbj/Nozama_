import numpy as np
import csv
import random
import string
import time
import math

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genOrders(n):

    with open('data/AccountOrder.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        lastrow = []
        for row in spamreader:
            lastrow = row

    index = int(lastrow[0])

    with open('data/Account.csv', newline='') as accfile:
        accreader = csv.reader(accfile)
        accountids = []
        for row in accreader:
            accountids.append(row[0])

    newOrders = []
    while len(newOrders) < n:
        neword = []
        index += 1
        neword.append(index)
        neword.append(random.choice(accountids))
        neword.append(genTimeStampDefault())
        newOrders.append(neword)
    
    with open('data/AccountOrder.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in newOrders:
            writer.writerow(row)
    
    genOrderProducts(newOrders)
    return True


def genOrderProducts(ords):
    with open('data/Product.csv', newline='') as prodfile:
        prodreader = csv.reader(prodfile)
        data = []
        for row in prodreader:
            data.append(row)

    newAOPs = []
    for order in ords:
        for _ in range(random.randint(1,4)): # each order includes 1-4 products
            aop = []
            prod = random.choice(data)
            aop.append(order[0]) # add AccountOrder id to AccountOrderProduct record
            aop.append(prod[0]) # add product id
            aop.append(random.randint(1,4)) # add quantity
            aop.append(prod[3]) # add price of a single item??
            aop.append("in stock")
            start = time.mktime(time.strptime(order[2], "%x %X"))
            end = math.floor(time.time())
            a = genTimeStamp(start, end)
            b = genTimeStamp(start, end)
            aop.append(min(a, b)) # add shipped at
            aop.append(max(a, b)) # add delivered at
            newAOPs.append(aop)
    
    with open('data/AccountOrderProduct.csv', 'a', newline='') as aopfile:
        aopwriter = csv.writer(aopfile)
        for row in newAOPs:
            aopwriter.writerow(row)
    
    return True


def genTimeStampDefault():
    earliest = time.mktime(time.strptime('01/01/20 01:00:00', "%x %X"))
    latest = time.mktime(time.strptime('10/12/21 23:59:50', "%x %X"))
    tm = random.randint(earliest, latest)
    tm_struct = time.gmtime(tm)
    return time.strftime("%x %X", tm_struct)


def genTimeStamp(start, end):
    tm = random.randint(start, end)
    tm_struct = time.gmtime(tm)
    return time.strftime("%x %X", tm_struct)


if __name__ == "__main__":
    numNewOrders = 20
    genOrders(numNewOrders)
