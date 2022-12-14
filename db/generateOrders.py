import numpy as np
import csv
import random
import string
import time
import math
import uuid

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genOrders(n):


    # parse through existing Accounts to identify the UUIDs that exist and can have orders linked to them
    with open('data/Account.csv', newline='') as accfile:
        accreader = csv.reader(accfile)
        accountuuids = []
        for row in accreader:
            accountuuids.append(row[0])

    newOrders = []
    while len(newOrders) < n:
        neword = []
        index = uuid.uuid4()
        neword.append(index)
        neword.append(random.choice(accountuuids))
        neword.append(genTimeStampDefault())
        newOrders.append(neword)
    
    with open('data/AccountOrder.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='unix')
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
    
    with open('data/ProductInventory.csv', newline='') as invfile:
        invreader = csv.reader(invfile)
        inv = []
        for row in invreader:
            inv.append(row)

    newAOPs = []
    for order in ords:
        prodnum = random.randint(1,4) # each order includes 1-4 products
        prods = random.sample([prod[0] for prod in data], k=prodnum)
        for i in range(prodnum): 
            # find sellers of this prod
            currProdSellers = [pi[1] for pi in inv if pi[0]==prods[i]]
            print(currProdSellers)
            # choose to order from 1-2 dependant on how many sellers
            numSellersForProd = min(len(currProdSellers),2)
            for j in range(numSellersForProd):
                aop = []
                aop.append(order[0]) # add AccountOrder UUID to AccountOrderProduct record
                aop.append(prods[i]) # add product id
                aop.append(currProdSellers[j]) # add seller id
                aop.append(random.randint(1,4)) # add quantity
                aop.append("3.99") # add price of a single item??
                aop.append(random.choices(["Shipped", "Placed", "Delivered"], weights=[1,1,1], k=1)[0]) #add status
                start = time.mktime(time.strptime(order[2], "%x %X"))
                end = math.floor(time.time())
                a = genTimeStamp(start, end)
                b = genTimeStamp(start, end)
                aop.append(min(a, b)) # add shipped at
                aop.append(max(a, b)) # add delivered at
                newAOPs.append(aop)
    
    with open('data/AccountOrderProduct.csv', 'w') as aopfile:
        aopwriter = csv.writer(aopfile, dialect='unix')
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
