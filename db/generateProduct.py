import numpy as np
import csv
import random
import string

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genProducts(n):

    with open('data/Product.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        lastrow = []
        for row in spamreader:
            lastrow = row
        print(lastrow)

    index = int(lastrow[0])
    modifier = ['Lightly used', 'Handmade Italian', 'Free shipping', 'Blue', 'Red', 'Durable',
            'Award winning', 'Cheap', 'Walmart', 'Ikea']
    prods = ['basketball hoop', 'iPhone 7S case', 'wire whisk', 'nail polish', 'shelf'
            'leather briefcase', 'acrylic paint', 'posterboard', 'cutting board', 'soccer cleats']
    ends = ['.00', '.49', '.99' '.95']
    newProds = []

    while len(newProds) < n:
        newprod = []
        index += 1
        newprod.append(index)
        prod = random.choice(modifier) + " " + random.choice(prods)
        newprod.append(prod)
        newprod.append('desc') # IDK WHAT THIS FIELD IS - GENERALIZE!!
        newprod.append(str(random.randint(5,200)) + random.choice(ends))
        newprod.append(True)
        newprod.append(0) # ID OF SELLER - GENERALIZE!!
        print(newprod)
        newProds.append(newprod)
    
    with open('data/Product.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in newProds:
            writer.writerow(row)
    
    return True


if __name__ == "__main__":
    numNewProducts = 20
    genProducts(numNewProducts)
