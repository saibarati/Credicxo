import scrapy
from csv import DictReader

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    with open(r"C:/Users/Barathi/Desktop/Task/Amazon Scraping - Sheet1.csv", 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    temp = []
    for row in csv_dict_reader:
        temp.append(f"https://www.amazon.{row['country']}/dp/{row['Asin']}")
    def parse_keyword_response(self, response):
        for query in temp:
            url = query
           # yield scrapy.Request(url=url, callback=self.parse_keyword_response)
            yield scrapy.Request(url=url, callback=self.parse_product_page)

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
            di = json.loads(json_acceptable)
            sizes = di.get('size_name', [])
            colors = di.get('color_name', [])
        
        bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        seller_rank = response.xpath('//*[text()="Amazon Best Sellers Rank:"]/parent::*//text()[not(parent::style)]').extract()
        yield { 'Title': title, 'MainImage': image, 'Price': price,  'Description': description }
