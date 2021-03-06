# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# Items - definicja pol
class SearchPageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    object_name = scrapy.Field()
    price = scrapy.Field()
    button_name = scrapy.Field()
    website_link = scrapy.Field()
    number_of_shops = scrapy.Field()
    pass
