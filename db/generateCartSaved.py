import numpy as np
import csv
import random
import string
import uuid
import statistics

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genCart(n, userIDs, prodIDs, currCarts):
    
    newCart = zip(random.choices(userIDs, k=(n * len(userIDs))), random.choices(prodIDs, k=(n * len(userIDs))))
    with open('data/CartProduct.csv', 'w') as cpfile:
        writer = csv.writer(cpfile, dialect='unix')
        for row in newCart:
            # elements stringified when read from file
            if [str(row[0]), str(row[1])] not in currCarts:
                currCarts.append([str(row[0]), str(row[1])])
                writer.writerow([str(row[0]), str(row[1]), random.randint(1,4)])
    return True


def genSaved(n, userIDs, prodIDs, currSaved):
    
    newSaves = zip(random.choices(userIDs, k=(n * len(userIDs))), random.choices(prodIDs, k=(n * len(userIDs))))
    with open('data/SavedProduct.csv', 'w') as sfile:
        writer = csv.writer(sfile, dialect='unix')
        for row in newSaves:
            # elements stringified when read from file
            if [str(row[0]), str(row[1])] not in currSaved:
                currSaved.append([str(row[0]), str(row[1])])
                writer.writerow(row)
    return True


def readCSVs():
    with open('data/Product.csv', newline='') as pfile:
        preader = csv.reader(pfile)
        prods = []
        for row in preader:
            prods.append(row[0])
    
    with open('data/Account.csv', newline='') as accfile:
        accreader = csv.reader(accfile)
        accs = []
        for row in accreader:
            accs.append(row[0])
    
    with open('data/CartProduct.csv', newline='') as cartfile:
        cartreader = csv.reader(cartfile)
        carts = []
        for row in cartreader:
            carts.append(row[0:2])
    
    with open('data/SavedProduct.csv', newline='') as savefile:
        savereader = csv.reader(savefile)
        saves = []
        for row in savereader:
            saves.append(row)
    return [accs, prods, carts, saves]


def genCartSaved(n):
    [users, prods, carts, saved] = readCSVs()
    genCart(n, users, prods, carts)
    genSaved(n, users, prods, saved)

if __name__ == "__main__":
    numProdPerAccount = 3
    genCartSaved(numProdPerAccount)
