# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import FormRequest

from data_collection.items import ChamberOfDeputiesSession as Session


class ChamberOfDeputiesSessionsSpider(scrapy.Spider):
    name = 'chamber_of_deputies_sessions'
    allowed_domains = ['camara.leg.br']
    start_urls = [(
        'http://www2.camara.leg.br'
        '/atividade-legislativa/plenario/resultadoVotacao'
    )]

    def parse(self, response):
        iframe_url = response.css('#ifr::attr("src")').extract_first()
        yield scrapy.Request(iframe_url, callback = self.parse_iframe)

    def parse_iframe(self, response):
        selector = (
            '//div[contains(concat(" ", @class, " "), " caixaDownload ")]'
            '//a[contains(text(),"legislatura")]'
        )
        urls = response.xpath(selector).xpath('@href').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_download_page)

    def parse_download_page(self, response):
        files = response.css('[name="liste1"] option::attr("value")').extract()
        urls = []
        for filename in files:
            url = response.url.split('/')
            url[-1] = filename
            urls.append('/'.join(url))
        return Session(file_urls=urls)
