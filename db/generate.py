from generateAccount import genUsers
from generateProduct import genProductsAndTags, genImage
from generateOrders import genOrders
from generateCartSaved import genCartSaved
from generateReview import genReview
import numpy as np
import csv
import random
import string
import time
import math


def generate():

    numNewUser = 10
    numNewProduct = 20
    numNewOrder = 20
    numNewReview = 20
    numProdPerAccount = 3

    genUsers(numNewUser)
    genProductsAndTags(numNewProduct)
    genImage()
    genOrders(numNewOrder)
    genCartSaved(numProdPerAccount)
    genReview(numNewReview)

if __name__ == "__main__":
    generate()