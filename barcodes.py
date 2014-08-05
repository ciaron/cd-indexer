# -*- coding: utf-8 -*-
"""
1. Read barcode CSV file output by Barcode Scanner (ZXing Team) Android app.
2. Look up UPC code on upc-search.org (XML pay-for API: http://www.ean-search.org/ean-database-api.html)
   - can also just scrape the HTML
3. Create static HTML page (product image, artist, album title etc. for music CDs) 
"""

# AMAZON affiliate:
# DE associate tag: ciaronnet-21
import csv, sys
from time import sleep
import fileinput
from amazon.api import AmazonAPI, AsinNotFound
from AWS import AWSAccessKeyId, AWSSecretKey, AWSAssociateTag
amazon_com = AmazonAPI(AWSAccessKeyId, AWSSecretKey, AWSAssociateTag, region='US')
amazon_co_uk = AmazonAPI(AWSAccessKeyId, AWSSecretKey, AWSAssociateTag, region='UK')
amazon_de = AmazonAPI(AWSAccessKeyId, AWSSecretKey, AWSAssociateTag, region='DE')

# Read the CSV file (barcodes.csv)
barcodes = []
#with open('barcodes-short.csv', 'rb') as csvfile:
#    reader=csv.reader(csvfile)
#    for row in reader:
#        barcodes.append(row[0])
for row in csv.reader(iter(sys.stdin.readline, '')):
    barcodes.append(row[0])

#print barcodes
results = {}
count = 0

print "---"
print "title: CDs to give away"
print "layout: default"
print "cds:"

for ItemId in barcodes:

    sleep(1.0)
    if len(str(ItemId)) == 12:
        IdType = 'UPC'
    elif len(str(ItemId)) == 13:
        IdType = 'EAN'
    else:
        IdType = 'unknown'

    if IdType != 'unknown':

        try:
            product = amazon_co_uk.lookup(SearchIndex='All', IdType=IdType, ItemId=ItemId)
        except AsinNotFound:
            try:
                product = amazon_com.lookup(SearchIndex='All', IdType=IdType, ItemId=ItemId)
            except:
                try:
                    product = amazon_de.lookup(SearchIndex='All', IdType=IdType, ItemId=ItemId)
                except:
                    print "%s not found" % ItemId

        count += 1
        results[ItemId] = {}

        try:
            results[ItemId]['artist'] = product.item.ItemAttributes.Artist.text.encode('utf-8')
        except:
            results[ItemId]['artist'] = 'unknown'
        try:
            results[ItemId]['title'] = product.title
        except:
            results[ItemId]['title'] = 'unknown'
        try:
            if product.small_image_url != None:
                results[ItemId]['image'] = product.small_image_url
            else:
                results[ItemId]['image'] = 'http://placehold.it/75x75'

        except:
           results[ItemId]['image'] = 'http://placehold.it/75x75'
        try:
           results[ItemId]['offer_url'] = product.offer_url
        except:
           results[ItemId]['offer_url'] = 'http://amazon.de'

        print "    - artist: " + results[ItemId]['artist']
        print "      title: " + results[ItemId]['title']
        print "      img_url: " + results[ItemId]['image']
        print "      url: " + results[ItemId]['offer_url'] 

    else:
        #print "Unknown IdType for %s, skipping" % ItemId
        pass

print "---"
