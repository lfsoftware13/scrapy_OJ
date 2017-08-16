import scrapy
from database.constants import CODEFORCE_DOMAIN


def getPage(response):
    if not isinstance(response, scrapy.http.Response):
        return ()

    pageSpans = response.xpath("//span[contains(@class, 'page-index')]")
    pageActSpans = response.xpath("//span[contains(@class, 'page-index') and contains(@class, 'active')]")
    pageNextSpans = response.xpath("//span[contains(@class, 'page-index') and contains(@class, 'active')]/../following-sibling::li[1]/span[contains(@class, 'page-index')]")

    if len(pageSpans) == 0:
        return (0, 0, 0, 0, None, None, None, None)

    pageAct = 0
    pageActUrl = None
    if len(pageActSpans) > 0:
        pageAct = pageActSpans[0].xpath("a/text()").extract()[0]
        pageActUrl = CODEFORCE_DOMAIN + pageActSpans[0].xpath("a/@href").extract()[0]

    pageNext = 0
    pageNextUrl = None
    if len(pageNextSpans) > 0:
        pageNext = pageNextSpans.xpath("a/text()").extract()[0]
        pageNextUrl = CODEFORCE_DOMAIN + pageNextSpans.xpath("a/@href").extract()[0]

    firstPage = pageSpans[0].xpath("a/text()").extract()[0]
    firstPageUrl = CODEFORCE_DOMAIN + pageSpans[0].xpath("a/@href").extract()[0]
    lastPage = pageSpans[-1].xpath("a/text()").extract()[0]
    lastPageUrl = CODEFORCE_DOMAIN + pageSpans[-1].xpath("a/@href").extract()[0]

    return (firstPage, lastPage, pageAct, pageNext, firstPageUrl, lastPageUrl, pageActUrl, pageNextUrl)


def getCurrentPage(response):
    pageList = getPage(response)

    if len(pageList) == 3:
        return pageList[2]
    return None
