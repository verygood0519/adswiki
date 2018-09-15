# -*- coding: utf-8 -*-
import scrapy

from adswiki.items import AdswikiItem


class AdswikiSpiderSpider(scrapy.Spider):
    name = 'adswiki_spider'
    allowed_domains = ['adswiki.net']
    start_urls = ['http://www.adswiki.net/ads_wiki/cpccpm-networks']

    def parse(self, response):
        page_count = response.css('.pages::text').extract_first()
        page_count = int(str.strip(page_count.split('/')[1]))
        for index in range(1, page_count + 1):  # page_count + 1
            get_url = 'http://www.adswiki.net/ads_wiki/cpccpm-networks/page/' + str(index)
            print('page:' + str(index))
            yield scrapy.Request(url=get_url, callback=self.parse_adswiki)
            break

    def parse_adswiki(self, response):
        titles = response.css('.entry-title')
        for title in titles:
            name = title.css('a::text').extract_first()
            if 'closed' not in name.lower():
                get_url = title.css('a::attr(href)').extract_first()
                yield scrapy.Request(url=get_url, callback=self.parse_adswiki_item)

    def parse_adswiki_item(self, response):
        entry_title = response.css('.entry-title::text').extract_first()
        href = response.css('.bottom a::attr(href)').extract_first()
        afftable = response.css('.afftable')
        Commission_Type = afftable.xpath('//tr[2]/td[2]/text()').extract_first(default='')
        Minimum_Payment = afftable.xpath('//tr[3]/td[2]/text()').extract_first(default='')
        Payment_Frequency = afftable.xpath('//tr[4]/td[2]/text()').extract_first(default='')
        Payment_Method = afftable.xpath('//tr[5]/td[2]/text()').extract_first(default='')
        Country = afftable.xpath('//tr[6]/td[2]/text()').extract_first(default='')
        # Contact = response.xpath('//*[@id="post-11311"]/div[2]/div[1]/div[3]/table/tbody/tr[7]/td[2]').extract()

        yield scrapy.Request(url=href, callback=self.parse_adswiki_item2, meta={
            'entry_title': entry_title,
            'Commission_Type': Commission_Type,
            'Minimum_Payment': Minimum_Payment,
            'Payment_Frequency': Payment_Frequency,
            'Payment_Method': Payment_Method,
            'Country': Country
        })

    def parse_adswiki_item2(self, response):
        get_url = 'https://www.alexa.com/siteinfo/' + response.url
        yield scrapy.Request(url=get_url, callback=self.parse_adswiki_alexa, dont_filter=True,
                             meta={
                                 'entry_title': response.meta['entry_title'],
                                 'ads_url': response.url,
                                 'Commission_Type': response.meta['Commission_Type'],
                                 'Minimum_Payment': response.meta['Minimum_Payment'],
                                 'Payment_Frequency': response.meta['Payment_Frequency'],
                                 'Payment_Method': response.meta['Payment_Method'],
                                 'Country': response.meta['Country']
                             }
                             )

    def parse_adswiki_alexa(self, response):
        globleRank = 0
        globleRanks = response.xpath(
            '//*[@id="traffic-rank-content"]/div/span[2]/div[1]/span/span/div/strong/text()').extract()
        countryRankName = response.css('.countryRank .metrics-title a::text').extract_first(default='')
        countryRank = response.xpath(
            '//*[@id="traffic-rank-content"]/div/span[2]/div[2]/span/span/div/strong/text()').extract_first(default='')
        countryRank = str.strip(countryRank).replace('\\n', '').replace(',', '')
        if len(globleRanks) == 2:
            globleRank = str.strip(globleRanks[1]).replace('\\n', '').replace(',', '')

        if (str.strip(countryRank) != ''):
            item = AdswikiItem()
            item['entry_title'] = str.strip(response.meta['entry_title'])
            item['ads_url'] = str.strip(response.meta['ads_url'])
            item['Commission_Type'] = str.strip(response.meta['Commission_Type'])
            item['Minimum_Payment'] = str.strip(response.meta['Minimum_Payment'])
            item['Payment_Frequency'] = str.strip(response.meta['Payment_Frequency'])
            item['Payment_Method'] = str.strip(response.meta['Payment_Method'])
            item['Country'] = str.strip(response.meta['Country'])
            item['globleRank'] = int(str.strip(globleRank))
            item['countryRankName'] = str.strip(countryRankName)
            item['countryRank'] = int(str.strip(countryRank))
            yield item
        # print(globleRank, countryRankName, countryRank)
