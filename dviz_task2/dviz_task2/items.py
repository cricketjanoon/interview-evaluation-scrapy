# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DvizTask2Item(scrapy.Item):
    # define the fields for your item here like:
    product = scrapy.Field()
    sub_category = scrapy.Field()
    prod_names = scrapy.Field()
    descriptions = scrapy.Field()
