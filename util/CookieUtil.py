import scrapy


def getCookieObject(response):
    if not isinstance(response, scrapy.http.Response):
        return None

    cookie_ob = {}
    cookies = response.headers.getlist('Set-Cookie')

    for co in cookies:
        strs = co.decode('gbk').split('=', 1)
        cookie_ob[strs[0]] = strs[1]
    return cookie_ob