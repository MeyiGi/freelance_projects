import scrapy


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["thestellariscollection.com"]
    start_urls = ["https://www.thestellariscollection.com/store"]

    def parse(self, response):
        product_links = response.css(".grid-item a::attr('href')").getall()
        yield from response.follow_all(product_links, self.parse_product)

    def parse_product(self, response):
        
        if response.css(".sold-out").get():
            self.logger.info(f"skipping sold-out product: {response.url}")
            return 
        
        self.logger.info(response.url)

        def parse_specific(target):
            description = response.css(".ProductItem-details-excerpt p::text").getall()

            if target == "collection":
                try:
                    return description[0]
                except Exception as e:
                    return ""
                
            if target in ["condition", "box", "warranty"]:
                for it in description:
                    if target in it:
                        if target == "warranty":
                            return it.strip(".")[-1].strip()
                        return it.split(".")[0].strip()
                    
                return ""
            
            for it in description:
                if target in it:
                    return it.split(":")[-1].strip()
                
            return ""
        
        item = {}

        item["title"] = response.css(".ProductItem-details-title::text").get()
        item["condition"] = parse_specific("condition")
        item["box, paper, tags, card, other (multiple)"] = parse_specific("box")
        item["manufacturer"] = parse_specific("Brand")
        item["collection"] = parse_specific("collection")
        item["reference-number"] = parse_specific("Reference Number")
        item["Year of Production"] = parse_specific("Year of Production")
        item["Case Size"] = parse_specific("Case Size")
        item["Case Material"] = parse_specific("Case Material")
        item["band-material"] = parse_specific("Bracelet Material")
        item["dial-color"] = parse_specific("Dial")
        item["case"] = item["Case Material"] + "\n" + item["Case Size"] + "\n" + parse_specific("Case Thickness")
        item["bezel"] = ""
        item["bezel-material"] = parse_specific("Bezel")
        item["warranty"] = parse_specific("warranty")
        item["website-url"] = response.url

        images = response.css('.ProductItem-gallery-slides-item img.ProductItem-gallery-slides-item-image::attr("data-src")').getall()
        for i in range(20):
            try:
                item[f"image-{i}"] = images[i]
            except Exception as e:
                item[f"image-{i}"] = ""

        yield item

