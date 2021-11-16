import numpy as np
import csv
import random
import string
import uuid

# IN ORDER TO WORK, CSVs MUST END IN NEWLINE!
def genProductsAndTags(n):

    # define adjectives for combinational product generation
    modifier = ['Lightly used', 'Handmade Italian', 'Free shipping', 'Blue', 'Red', 'Durable',
            'Award winning', 'Cheap', 'Walmart', 'Ikea', 'Affordable', 'Great', 'Elite', 'Bespoke',
            'Collectors', 'Imported']
    
    # define base products, with the tags to be associated
    # (tags do not need to exist in database; they'll be added)
    prods = {'basketball hoop': ['sports'], 
    'iPhone 7S case': ['technology'], 
    'wire whisk': ['food', 'cooking'], 
    'nail polish': ['beauty'], 
    'shelf': ['decor', 'furniture'], 
    'leather briefcase': ['beauty'], 
    'acrylic paint': ['art'], 
    'posterboard': ['art'], 
    'cutting board': ['food'], 
    'soccer cleats': ['sports'],
    'textbook' : ['education', 'office supplies'],
    'record player' : ['furniture', 'music'],
    'mirror' : ['beauty', 'furniture', 'decor'],
    'ray gun' : ['technology'],
    'hockey mask' : ['sports'],
    'bitcoin' : ['technology'],
    'stapler' : ['office supplies'],
    'mug' : ['cooking', 'food'],
    'mask' : ['cooking'],
    'pillow' : ['cooking', 'decor'],
    'steak knives' : ['cooking'],
    'paint brush' : ['art'],
    'glitter pen' : ['art', 'office supplies'],
    'baseball goal' : ['sports', 'furniture'],
    'lightning charger': ['technology', 'office supplies'] 
    }

    # define cent cost of randomly generated prices
    ends = ['.00', '.49', '.99', '.95', '.45', '.89']
    newProds = []
    newTags = []
    newProdTags = []

    #read data from other files with helper method
    existingTags = {}
    tagIndex = 0
    existingPTs = []

    while len(newProds) < n:
        newprod = []
        index = uuid.uuid4()
        newprod.append(index) # add UUID as 0th element
        mod = random.choice(modifier) 
        prod = random.choice(list(prods.keys()))
        
        for v in prods[prod]:
            # for each tag associated with the base product:
            # check if the tag exists
            # add it if not
            if v not in existingTags.keys():
                existingTags[v] = tagIndex
                newTags.append([tagIndex, v])
                tagIndex += 1
            # then repeat for product tag
            currPT = existingTags[v]
            if [currPT, index] not in existingPTs and [currPT, index] not in newProdTags:
                newProdTags.append([currPT, index])
            
        prodstring = mod + ' ' + prod
        newprod.append(prodstring) # add product name as 1st element
        newprod.append(genDesc(prodstring)) # add product description with helper method as 2nd element
        newprod.append(str(random.randint(5,200)) + random.choice(ends)) # add price as 3rd element
        newprod.append(random.choices([True, False], weights=[0.8, 0.2])[0]) # add randomly generated availability as 4th element
        # print(newprod)
        newProds.append(newprod)
    
    # write data to CSVs with helper method
    write(newProds, newTags, newProdTags)
    genImage(newProds)
    genInventory(newProds)
    return True


def genDesc(prodstring):
    words = [' great reviewed product', ' best', ' highly-rated product', ' e-commerce product', ' you should purchase',
    ' comes with warranty', ' enhance your life', ' act fast', ' hand made', ' tried and tested', ' patended', ' lifetime warrenty',
    ' batteries not included', ' great as a gift', ' and', ' lowest price', ' match any price', ' Also!', ' great']
    return 'This beautiful ' + prodstring + ' '.join(random.choices(words, k=(random.randint(0,3))))


def genImage(newprods):
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
    'soccer cleats': "https://static.nike.com/a/images/t_PDP_1280_v1/f_auto,q_auto:eco/309882d1-4ba4-4516-809e-3bac304ad450/phantom-gt-elite-3d-fg-firm-ground-soccer-cleats-2clxTj.png",
    'textbook' : "https://campussuite-storage.s3.amazonaws.com/prod/1559033/fab8744a-ab41-11ea-9bfa-127f10bcdb1b/2163877/8bff308c-0183-11eb-8d43-0a2f7cee82b1/optimizations/2097152",
    'record player' : "https://m.media-amazon.com/images/I/7107fFqeFMS._AC_SL1500_.jpg",
    'mirror' : "https://cdn.arhaus.com/product/StandardV2/651926M0239_3.jpg?preset=ProductLarge",
    'ray gun' : "https://m.media-amazon.com/images/I/71WMnWQqbSL._SL1500_.jpg",
    'hockey mask' : "https://m.media-amazon.com/images/I/51nzM6R17CL._AC_UX385_.jpg",
    'bitcoin' : "https://img.etimg.com/thumb/msid-85584610,width-640,resizemode-4,imgsize-29562/4-bitcoin-gold.jpg",
    'stapler' : "https://m.media-amazon.com/images/I/61qkoldpK+L._AC_SL1000_.jpg",
    'mug' : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTw-kaLvB6gwmGcNQtKbWU7HPXSR5Gdoh5Mpw&usqp=CAU",
    'mask' : "https://www.adesso.com/wp-content/uploads/2020/06/PPE-100_1.jpg",
    'pillow' : "https://rnb.scene7.com/is/image/roomandboard/452325?scl=1",
    'steak knives' : "https://cdn.shopify.com/s/files/1/1786/7137/products/KnifeSet_1100x.jpg?v=1618898839",
    'paint brush' : "https://shop.harborfreight.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/6/2/62676_zzz_500.jpg",
    'glitter pen' : "https://imgprd19.hobbylobby.com/9/f7/00/9f700c0821d61711eeafe855d67f1404139613f2/700Wx700H-1688753-052919.jpg",
    'baseball goal' : "https://cdn3.volusion.com/xmqo7.amhs2/v/vspfiles/photos/PNET-77NET-2.jpg?v-cache=1462453165",
    'lightning charger' : "https://m.media-amazon.com/images/I/51dK6Od0J2L._AC_SL1500_.jpg"
    }

    
    nextRows = []
    for prod in newprods:
        flag = False
        for k,v in urls.items():
            if k in prod[1] and not flag:
                nextRows.append([prod[0], v])
                flag = True
        if flag == False:
            nextRows.append([prod[0], other])

    
    with open('data/ProductImage.csv', 'w') as imgfilew:
        writer = csv.writer(imgfilew, dialect='unix')
        for row in nextRows:
            writer.writerow(row)
    return True


def genInventory(prods):
    sellers = readCSVs()
    newProdInv = []
    for prod in prods:
        #each product is sold by 1-4 sellers
        numSellers = random.randint(1,4)
        sells = random.sample(sellers, k=numSellers)
        for i in range(numSellers):
            currProdInv = []
            currProdInv.append(prod[0])
            currProdInv.append(sells[i][0])
            if prod[4]:
                currProdInv.append(random.randint(1,300))
            else:
                currProdInv.append(0)
            newProdInv.append(currProdInv)

    with open('data/ProductInventory.csv', 'w') as pifile:
        piwriter = csv.writer(pifile, dialect='unix')
        for row in newProdInv:
            piwriter.writerow(row)
    return True


def write(prods, tags, prodtags):
    with open('data/Product.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, dialect='unix')
        for row in prods:
            writer.writerow(row)
    
    with open('data/Tag.csv', 'w') as tfile:
        writer = csv.writer(tfile, dialect='unix')
        for row in tags:
            writer.writerow(row)
    
    with open('data/ProductTag.csv', 'w') as writeptfile:
        writer = csv.writer(writeptfile, dialect='unix')
        for row in prodtags:
            writer.writerow(row)
    return True


def readCSVs():
    with open('data/Tag.csv', newline='') as tagfile:
        tagreader = csv.reader(tagfile)
        existingTags = {}
        tagIndex = 0
        for row in tagreader:
            existingTags[row[1]] = row[0]
            tagIndex = int(row[0])
        tagIndex += 1
    
    with open('data/ProductTag.csv', newline='') as ptfile:
        ptreader = csv.reader(ptfile)
        existingPTs = []
        for row in ptreader:
            existingPTs.append(row)
    
    with open('data/Seller.csv', newline='') as sellfile:
        sellreader = csv.reader(sellfile)
        sells = []
        for row in sellreader:
            sells.append(row) 
    return sells


if __name__ == "__main__":
    numNewProducts = 20
    genProductsAndTags(numNewProducts)
