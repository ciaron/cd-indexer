# A barcode-scanner-to-HTML-index thingy.

## Requires:

1. Python
2. python-amazon-simple-product-api (pip install...)
3. An Amazon affililate account (for Associate Tag)
4. A Jekyll installation for generating the static HTML

## Running:
1. python barcode.py < barcode.csv > html/index.md
2. cd html
3. jekyll build - this puts everything into _site. Copy that to your webserver. Bootstrap 3.2 is included for styling.

An example barcode.csv file is supplied. This format is from the free/awesome ZXing Android app "Barcode Scanner". Only the first column is needed, which is a UPC or EAN code from the scanner.