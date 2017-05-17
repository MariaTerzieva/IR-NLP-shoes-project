# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ShopsectorItem(Item):
    link = Field()
    title = Field()
    photo = Field()
    price = Field()
    colors = Field()
    sizes = Field()
    gender = Field()
