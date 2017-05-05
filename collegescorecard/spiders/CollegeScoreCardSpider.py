# -*- coding: utf-8 -*-
import scrapy
from collegescorecard.items import CollegeScoreCardItem
from bs4 import BeautifulSoup
from datetime import datetime
from collegescorecard.mongodal import MongoDAL
from time import sleep
from scrapy.selector import Selector
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import json

class CollegeScoreCardSpider(scrapy.Spider):
    name = "collegescorecardspider"
    allowed_domains = ["collegescorecard.ed.gov"]
    base_url = "https://api.data.gov/ed/collegescorecard/v1/schools/?sort=2014.student.size%3Aasc&school.operating=1&2014.student.size__range=0..&2014.academics.program_available.assoc_or_bachelors=true&school.degrees_awarded.predominant__range=1..3&school.degrees_awarded.highest__range=2..4&fields=id%2Cschool.name%2Cschool.city%2Cschool.state%2C2014.student.size%2Cschool.ownership%2Cschool.degrees_awarded.predominant%2C2014.cost.avg_net_price.overall%2C2014.completion.rate_suppressed.overall%2C2012.earnings.10_yrs_after_entry.median%2C2012.earnings.6_yrs_after_entry.percent_greater_than_25000%2Cschool.under_investigation&api_key=A79LCGIbqJYhpvRfggnQ9KhBBhQWyoAJJwu1H3Ph&per_page=100&page="
    pageid = 0
    max_pageid = 1
    download_delay = 0.25
    start_urls = [base_url + str(pageid)]


    

    def parse(self, response):

        jsonresponse = json.loads(response.body)

        if self.max_pageid == 1:
           self.max_pageid = int(int(jsonresponse["metadata"]["total"])/100)    

        for scholarship in jsonresponse["results"]:
        
            item = CollegeScoreCardItem()
            try:
                item['University_Name'] = scholarship["school.name"].strip()
            except:
                item['University_Name'] = ''
                pass

            try:
                item['City_State'] = scholarship["school.city"].strip()+ ', ' + scholarship["school.state"].strip()
            except:
                item['City_State'] = ''
                pass 
                
            try:
                item['Number_Of_Undergraduates'] = scholarship["2014.student.size"]
            except:
                item['Number_Of_Undergraduates'] = 0
                pass  
                
                          
            yield item
            
        if self.pageid <= self.max_pageid:
            self.pageid = self.pageid + 1    
            next_page = self.base_url + str(self.pageid)

            yield scrapy.Request(url=next_page, callback=self.parse,meta={'dont_merge_cookies': False},dont_filter=True,encoding='utf-8'\
            ,errback=self.errback,headers={'Referer':None})    

    def errback(self, response):
        pass

"""            

"""

"""
#configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(StudyInChinaSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished
"""