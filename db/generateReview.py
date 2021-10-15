import numpy as np
import csv
import random
import string
import time
import math

with open('data/Account.csv', newline='') as accfile:
        accreader = csv.reader(accfile)
        accountuuids = []
        for row in accreader:
            accountuuids.append(row[0])

def genReview(n);

    starter = ['This product', 'My purchase', 'This', 'It', 'Do not.', 'I am buying more! It']
    verb = ['is the', 'was the', 'will be the']
    adj = ['best ever', 'worst ever', 'biggest waste of money', 'best purchase I made', 'least helpful', 'most helpful', 'worst quality', 'most amazing quality']
    title = ['AMAZING', 'Disaster', 'Do not buy this', 'I recommend this', 'Undecided on the']
    extra = ['product', 'item', '!', 'thing']
    newReview = []

    while len(newReview) < n:
        review = []
        index = uuid.uuid4()
        review.append(index)
        review.append(random.choice(accountuuids))
        name = random.choice(title) + " " + random.choice(extra)
        review.append(name)
        sentence = random.choice(starter) + " " + random.choice(verb) + " " + random.choice(adj)
        review.append(sentence)
        t1 = genTimeStampDefault()
        t2 = genTimeStampDefault()
        review.append(min(t1, t2)) 
        review.append(max(t1, t2)) 
        review.append(random.randint(1,5))
        print(review)
        newReview.append(review)
    with open('data/Review.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in newReview:
            writer.writerow(row)
    
    return True


def genTimeStampDefault():
    earliest = time.mktime(time.strptime('01/01/20 01:00:00', "%x %X"))
    latest = time.mktime(time.strptime('10/12/21 23:59:50', "%x %X"))
    tm = random.randint(earliest, latest)
    tm_struct = time.gmtime(tm)
    return time.strftime("%x %X", tm_struct)


if __name__ == "__main__":
    numNewReview = 20
    genOrders(numNewReview)
