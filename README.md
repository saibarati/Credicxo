# Credicxo

Python Scrapy spider searches Amazon using urls, extracts each products Title, Image url, price and description and scrape all the product information and returning the output in json format.

Make sure Scrapy is installed:

pip install scrapy

Creating a project:

scrapy startproject ecommerce_scraper


Execution steps:

1) Create a google spreadsheet csv data as Amazon Scraping - Sheet1
2) Read Amazon Scraping - Sheet1.csv file.
3) Looping the Asin and country parameters and passing to amazon url.

Amazon Spider:
The spider has 4 parts:

start_requests - will send a search query Amazon with a particular keyword.
parse_keyword_response - will extract the ASIN value for each product returned in the Amazon keyword query, then send a new request to Amazon to return the product page of that product. It will also move to the next page and repeat the process.
parse_product_page - will extract all the target information from the product page.

def parse_keyword_response(self, response):
  for query in temp:
      url = query
     # yield scrapy.Request(url=url, callback=self.parse_keyword_response)
      yield scrapy.Request(url=url, callback=self.parse_product_page)
      
If you want to scrape more or less fields on the product page then edit the XPath selectors in the parse_product_page function:

def parse_product_page(self, response):
    title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
    image_url = re.search('"large":"(.*?)"',response.text).groups()[0]
    price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
    description =response.xpath('//*[@id="productDescription"]/text()').extract_first()
    if not price:
        price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
                response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first()
    temp = response.xpath('//*[@id="twister"]')
        sizes = []
        colors = []
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
        
        yield { 'Title': title, 'MainImage': image, 'Price': price,  'Description': description }
 
