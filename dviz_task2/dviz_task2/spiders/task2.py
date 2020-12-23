import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from ..items import DvizTask2Item


class Task2Spider(scrapy.Spider):
    name = 'task2'
    start_urls = ["https://www.st.com/content/st_com/en.html"]

    def parse_details(self, response):

        prod_name = response.meta['prod_name']
        sub_prod = response.meta['sub_prod']
        names = response.css('[id="selector-links"] li a::text').extract()
        descriptions = response.css('[id="selector-links"] li div::text').extract()

        item = DvizTask2Item()
        item['product'] = prod_name
        item['sub_category'] = sub_prod
        item['prod_names'] = names
        item['descriptions'] = descriptions

        return item


    def parse(self, response):
        products = response.css("#st-site > div.off-canvas-wrap > div.inner-wrap > header > nav > div > div > ul:nth-child(1) > li:nth-child(1) > div > div > div.st-nav__submenu-list-container.js-st-nav-submenu-container > div");

        prod = products[0];

        for cat in products:
            prod_title =  cat.css("div.st-nav__subsubmenu-header > a::text")[0].extract().replace('Browse', '').strip()
            sub_cat = cat.css("div.st-nav__subsubmenu-container > div.st-nav__subsubmenu-wrapper.js-st-nav-subsubmenu-scroll > div div.st-nav__subsubmenu-grid > div.st-nav__subsubmenu-item")
            final_sub_texts = []
            final_sub_links = []
            for i in range(len(sub_cat)):
                has_more_sub_categories = sub_cat[i].css("ul")
                if has_more_sub_categories:
                    sub_sub_cats = sub_cat[i].css("ul li")
                    for j in range(len(sub_sub_cats)):
                        text = sub_sub_cats[j].css("a::text")[0].extract().strip()
                        link = sub_sub_cats[j].css("a").xpath("@href").extract()[0]
                        final_sub_texts.append(text)
                        final_sub_links.append("https://www.st.com/" + link + "#products")
                else:
                    text = sub_cat[i].css("div > a::text")[0].extract().strip()
                    link = sub_cat[i].css("div > a").xpath("@href").extract()[0]
                    final_sub_texts.append(text)
                    final_sub_links.append("https://www.st.com/"+link+"#products")


            print("--------------------------------------------------------------")
            print(prod_title)
            print(final_sub_texts)
            print(final_sub_links)
            print("--------------------------------------------------------------")

            # Now visit each link in the final_sub_links and extract name and description
            for k in range(len(final_sub_links)):
                sub_prod = final_sub_texts[k]
                url = final_sub_links[k]
                yield Request(url, callback=self.parse_details, meta={'prod_name': prod_title, 'sub_prod': sub_prod})

