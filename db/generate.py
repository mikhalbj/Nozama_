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

    numNewUser = 100
    numNewProduct = 200
    numNewOrder = 200
    numNewReview = 200
    numProdPerAccount = 4

    genUsers(numNewUser)
    genProductsAndTags(numNewProduct)
    genOrders(numNewOrder)
    genCartSaved(numProdPerAccount)
    genReview(numNewReview)

if __name__ == "__main__":
    generate()