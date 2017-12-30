# -*- coding: utf-8 -*-
import re

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
        yield scrapy.Request(iframe_url, callback=self.submit_search_query)

    def submit_search_query(self, response):
        return FormRequest.from_response(
            response,
            formdata={'datInicial': '01/01/2017', 'datFinal': '31/12/2017'},
            formname='form1',
            callback=self.parse_session_list,
        )

    def parse_session_list(self, response):
        selector = (
            '//ul[contains(concat(" ", @class, " "), " listaMarcada ")]'
            '//a[contains(text(), "votantes por UF")]'
        )
        urls = response.xpath(selector).xpath('@href').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_session)

    def parse_session(self, response):
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
        import ipdb; ipdb.set_trace()
        term = response.css('b::text').extract_first()
        term = re.findall('\d{4}', term)[0]
        files = response.css('[name="liste1"] option::attr("value")').extract()
        urls = []
        for filename in files:
            url = response.url.split('/')
            url[-1] = filename
            urls.append('/'.join(url))
        return Session(file_urls=urls, term=term)
