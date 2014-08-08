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

format='html' # use 'yaml' or 'html' depending on whether you want to process with Jekyll or not

# Read the CSV file (barcodes.csv)
barcodes = []
#with open('barcodes-short.csv', 'rb') as csvfile:
#    reader=csv.reader(csvfile)
#    for row in reader:
#        barcodes.append(row[0])
for row in csv.reader(iter(sys.stdin.readline, '')):
    barcodes.append(row[0])

#print barcodes
results = []
count = 0

if format=='yaml':
    print "---"
    print "title: CDs to give away"
    print "layout: default"
    print "cds:"
elif format=='html':
    from jinja2 import Template
    template_file = open('index.html.template')
    template = Template(template_file.read())
    template_file.close()

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
                    #print "%s not found" % ItemId
                    pass

        count += 1
        result = {}
        result['code'] = ItemId

        try:
            #result['artist'] = product.item.ItemAttributes.Artist.text.encode('utf-8')
            result['artist'] = product.item.ItemAttributes.Artist.text
        except:
            result['artist'] = 'unknown'

        try:
            result['title'] = product.title
        except:
            result['title'] = 'unknown'

        try:
            if product.small_image_url != None:
                result['image'] = product.small_image_url
            else:
                result['image'] = 'http://placehold.it/75x75'

        except:
           result['image'] = 'http://placehold.it/75x75'

        try:
           result['offer_url'] = product.offer_url
        except:
           result['offer_url'] = 'http://amazon.de'

        if format=='yaml':
            print "    - artist: " + result['artist']
            print "      title: " + result['title']
            print "      img_url: " + result['image']
            print "      url: " + result['offer_url']

        sys.stderr.write(unicode(result['artist']));
        sys.stderr.write(unicode(result['code']));
        sys.stderr.write('\n');
        results.append(result)

    else:
        #print "Unknown IdType for %s, skipping" % ItemId
        pass

if format == 'yaml':
    print "---"
elif format == 'html':
    sys.stderr.write('Rendering template...\n')
    sys.stdout.write(template.render(cds=results).encode( "utf-8" ))
