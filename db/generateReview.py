import numpy as np
import csv
import random
import string
import time
import math
import uuid


def genReview(n):
    accountuuids, produuids, selluuids = readreviews()
    imgurls = urls()
    sellerstarter = ['This shop', 'This seller', 'This account']
    starter = ['This product', 'My purchase', 'This', 'It', 'Do not.', 'I am buying more! It']
    verb = ['is the', 'was the', 'will be the']
    adj = ['best ever', 'worst ever', 'biggest waste of money', 'best purchase I made', 'least helpful', 'most helpful', 'worst quality', 'most amazing quality']
    title = ['AMAZING', 'Disaster', 'Do not buy this', 'I recommend this', 'Undecided on the']
    extra = ['product', 'item', '!', 'thing']
    sellerextra = ['seller', 'shop', '!', 'account']
    newReview = []
    newSellerReview = []
    newProductReview = []
    newReviewVote = []
    newProductImg = []

    while len(newReview) < n:
        vote = []
        review = []
        index = uuid.uuid4()
        review.append(index)
        review.append(random.choice(accountuuids))
        if random.choice([True, False]): # add image for half of reviews
            newProductImg.append([index, random.choice(imgurls)])
        decide = random.choice([True,False]) # determine a seller (false) vs a product (true) review
        if decide:
            myExtra = random.choice(extra)
            myStarter = random.choice(starter)
            newProductReview.append([index, random.choice(produuids)])
        else:
            myExtra = random.choice(sellerextra)
            myStarter = random.choice(sellerstarter)
            newSellerReview.append([index, random.choice(selluuids)])
        name = random.choice(title) + " " + myExtra #HERE
        review.append(name)
        sentence = myStarter + " " + random.choice(verb) + " " + random.choice(adj) #HERE
        review.append(sentence)
        t1 = genTimeStampDefault()
        t2 = genTimeStampDefault()
        review.append(min(t1, t2)) 
        review.append(random.choice([max(t1, t2), ''])) # some reviews shouldn't be edited
        review.append(random.randint(1,5))
        numvotes = random.randint(0,5)
        accounts = random.sample(accountuuids, k=numvotes) # can accounts vote on their own reviews?
        for i in range(numvotes): # add 0-5 votes for each review
            vote = []
            vote.append(accounts[i])
            vote.append(index)
            vote.append(random.choice([-1, 1]))
            newReviewVote.append(vote)
        print(review)
        newReview.append(review)
    
    writereviews(newReview, newReviewVote, newSellerReview, newProductReview, newProductImg)
    return True


def genTimeStampDefault():
    earliest = time.mktime(time.strptime('01/01/20 01:00:00', "%x %X"))
    latest = time.mktime(time.strptime('10/12/21 23:59:50', "%x %X"))
    tm = random.randint(earliest, latest)
    tm_struct = time.gmtime(tm)
    return time.strftime("%x %X", tm_struct)


def writereviews(newReview, newReviewVote, newSellerReview, newProductReview, newProductImg):
    with open('data/Review.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, lineterminator='')
        for row in newReview:
            writer.writerow("\n")
            writer.writerow(row)
    
    # should check if a review,vote tuple already exists in the file before writing?
    with open('data/ReviewVote.csv', 'a', newline='') as votefile:
        writer = csv.writer(votefile, lineterminator='')
        for row in newReviewVote:
            writer.writerow("\n")
            writer.writerow(row)
    
    with open('data/SellerReview.csv', 'a', newline='') as srfile:
        writer = csv.writer(srfile, lineterminator='')
        for row in newSellerReview:
            writer.writerow("\n")
            writer.writerow(row)

    with open('data/ProductReview.csv', 'a', newline='') as prfile:
        writer = csv.writer(prfile, lineterminator='')
        for row in newProductReview:
            writer.writerow("\n")
            writer.writerow(row)
    
    with open('data/ReviewImage.csv', 'a', newline='') as imgfile:
        writer = csv.writer(imgfile, lineterminator='')
        for row in newProductImg:
            writer.writerow("\n")
            writer.writerow(row)
    return True


def readreviews():
    with open('data/Account.csv', newline='') as accfile:
            accreader = csv.reader(accfile)
            accountuuids = []
            for row in accreader:
                accountuuids.append(row[0])

    with open('data/Product.csv', newline='') as prodfile:
            accreader = csv.reader(prodfile)
            produuids = []
            for row in accreader:
                produuids.append(row[0])

    with open('data/Seller.csv', newline='') as sellfile:
            accreader = csv.reader(sellfile)
            selluuids = []
            for row in accreader:
                selluuids.append(row[0])
    return [accountuuids, produuids, selluuids]


def urls():
    return ['https://grid.gograph.com/set-of-random-objects-eps-illustration_gg117533923.jpg',
    'https://thumbs.dreamstime.com/b/random-household-objects-collection-13040387.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRz-XAjlUXCKS0L156xpwl2lTmqhC8NAnjjvA&usqp=CAU',
    'https://thumbs.dreamstime.com/z/large-pop-art-collage-people-portraits-musical-instruments-random-objects-seamless-vector-background-136575400.jpg',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuvDHyTz99Q7gVRE4-Br7vyy2TDkeXKAw-3Q&usqp=CAU']


if __name__ == "__main__":
    numNewReview = 20
    genReview(numNewReview)
