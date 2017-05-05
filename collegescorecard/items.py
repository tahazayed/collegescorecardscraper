# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import six

class CollegeScoreCardItem(Item):
    University_Name = Field()
    City_State = Field()
    Number_Of_Undergraduates = Field()
    pass
    
 