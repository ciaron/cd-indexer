# A barcode-scanner-to-HTML-index thingy.

## Requires:

1. Python
2. python-amazon-simple-product-api (pip install...)
3. An Amazon affililate account (for Associate Tag)
4. For HTML: jinja2 templating system for Python (pip install...)
5. For Jekyll/YAML: A Jekyll installation for generating the static HTML

## Running (direct to HTML)
1. python barcode.py < barcode.csv > index.html

    This will output a HTML file based on the template index.html.template
    (requires Jinja2 - pip install jinja2)

## Running (Jekyll/YAML):
1. python barcode.py < barcode.csv > html/index.md

    This output is a YAML frontmatter section that can be parsed by Jekyll/Liquid.
2. cd html
3. jekyll build - this puts everything into _site. Copy that to your webserver. Bootstrap 3.2 is included for styling.

An example barcode.csv file is supplied. This format is from the free/awesome ZXing Android app [Barcode Scanner](https://play.google.com/store/apps/details?id=com.google.zxing.client.android&hl=en). Only the first column is needed, which is a UPC or EAN code from the scanner.
