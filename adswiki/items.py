# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class AdswikiItem(Item):
    entry_title = Field()
    ads_url = Field()
    Commission_Type = Field()
    Minimum_Payment = Field()
    Payment_Frequency = Field()
    Payment_Method = Field()
    Country = Field()
    globleRank = Field()
    countryRankName = Field()
    countryRank = Field()
