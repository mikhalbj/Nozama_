import numpy as np
import csv
import random
import string
import uuid

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genProducts(n):

    modifier = ['Lightly used', 'Handmade Italian', 'Free shipping', 'Blue', 'Red', 'Durable',
            'Award winning', 'Cheap', 'Walmart', 'Ikea']
    prods = ['basketball hoop', 'iPhone 7S case', 'wire whisk', 'nail polish', 'shelf',
            'leather briefcase', 'acrylic paint', 'posterboard', 'cutting board', 'soccer cleats']
    ends = ['.00', '.49', '.99' '.95']
    newProds = []

    while len(newProds) < n:
        newprod = []
        index = uuid.uuid4()
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

def genImage():
    other = "https://cdn.w600.comps.canstockphoto.com/pile-of-random-stuff-eps-vector_csp24436545.jpg"
    urls = {'basketball hoop': "https://cdn.shopify.com/s/files/1/0184/0106/7072/products/1_6_hoop_white_1024x1024.jpg?v=1597653738", 
    'iPhone 7S case': "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MKTT3?wid=1144&hei=1144&fmt=jpeg&qlt=80&.v=1623349387000", 
    'wire whisk': "https://m.media-amazon.com/images/I/61tN1JjOxZS._AC_SX466_.jpg", 
    'nail polish': "https://media.istockphoto.com/photos/nail-polish-picture-id821543718", 
    'shelf': "https://stattmann-11857.kxcdn.com/wp-content/uploads/2019/02/STnM_Unitmix03-601x900.jpg",
    'leather briefcase': "https://cdn.shopify.com/s/files/1/0373/9909/products/leather-palissy-briefcase-bag-cognac-grey-1b_grande.jpg?v=1630690561", 
    'acrylic paint': "https://modpodgerocksblog.com/wp-content/uploads/2012/02/Acrylic-paint.jpg", 
    'posterboard': "https://images.ctfassets.net/f1fikihmjtrp/73kRpUAw64xtJJ9uZMtB8C/62ed54b4a299401665eb30ec7b9e6f30/13100-1028-4ww.jpg?q=80&w=250", 
    'cutting board': "https://m.media-amazon.com/images/I/71rAPjgEJoL._AC_SX466_.jpg", 
    'soccer cleats': "https://static.nike.com/a/images/t_PDP_1280_v1/f_auto,q_auto:eco/309882d1-4ba4-4516-809e-3bac304ad450/phantom-gt-elite-3d-fg-firm-ground-soccer-cleats-2clxTj.png"}

    gooduuid = []
    with open('data/ProductImage.csv', newline='') as imgfile:
        reader = csv.reader(imgfile)
        for row in reader:
            gooduuid.append(row[0])
    
    newRows = []
    with open('data/Product.csv', newline='') as prodfile:
        reader = csv.reader(prodfile)
        for row in reader:
            if row[0] not in gooduuid:
                newRows.append([row[0], row[1]])
    
    nextRows = []

    for uuid in newRows:
        flag = False
        for k,v in urls.items():
            if k in uuid[1]:
                nextRows.append([uuid[0], v])
                flag = True
        if flag == False:
            nextRows.append([uuid[0], other])
    
    with open('data/ProductImage.csv', 'a', newline='') as imgfilew:
        writer = csv.writer(imgfilew)
        for row in nextRows:
            writer.writerow(row)

    return True



if __name__ == "__main__":
    numNewProducts = 20
    genProducts(numNewProducts)
    genImage()
