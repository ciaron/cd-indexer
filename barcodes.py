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
results = {}
count = 0

if format=='yaml':
    print "---"
    print "title: CDs to give away"
    print "layout: default"
    print "cds:"
elif format=='html':
    print """
<!DOCTYPE html>
<html lang="en" class="no-js">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CDs to give away...</title>
    <meta name="description" content="CDs to give away..." />
    <meta name="keywords" content="jekyll, python, CDs, giveaway" />
    <meta name="author" content="Ciaron Linstead" />

    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px;
      }
    </style>
    <!--<link href="/css/bootstrap-responsive.css" rel="stylesheet"> -->
  </head>
  <body>
<div class="navbar navbar-inverse navbar-fixed-top">
  <div class="navbar-inner">
    <div class="container">
      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
      <a class="navbar-brand" href="#">CDs to give away...</a>
      <div class="nav-collapse collapse">
        <ul class="nav">
          <li class="active"><a href="/">Home</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="container">

    <table class="table">

"""

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

        if format=='yaml':
            print "    - artist: " + results[ItemId]['artist']
            print "      title: " + results[ItemId]['title']
            print "      img_url: " + results[ItemId]['image']
            print "      url: " + results[ItemId]['offer_url']
        elif format=='html':
            print "<tr><td>"+str(count)+"</td><td><img src='" + results[ItemId]['image'] + "'/></td><td><a href='" + results[ItemId]['offer_url'] + "'>" + results[ItemId]['artist'] + " - " + results[ItemId]['title'] + "</a></td></tr>"

    else:
        #print "Unknown IdType for %s, skipping" % ItemId
        pass

if format == 'yaml':
    print "---"
elif format == 'html':
    print """
    </table>

</div>

Code for this site <a href="https://github.com/ciaron/cd-indexer">on Github</a>
  </body>
</html>
"""
