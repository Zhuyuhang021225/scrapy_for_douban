import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban.items import DoubanItem


class CollectSpider(CrawlSpider):
    name = "collect"
    user_id = input("输入你的豆瓣id:")
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        "https://movie.douban.com/people/{}/collect?start=0&sort=time&rating=all&filter=all&mode=grid".format(user_id)]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
        },
        'source': "collect",
        "user_id": str(user_id)
    }

    rules = (Rule(LinkExtractor(
        allow=r"/people/{}/collect\?start=\d+\&sort=time\&rating=all\&filter=all\&mode=grid".format(user_id)),
        callback="parse_item", follow=True),)

    def parse_item(self, response):
        item_list = response.xpath("//div[@class='item comment-item']")

        for item in item_list:
            image_url = item.xpath("./div/a/img/@src").extract_first()
            movie_name = item.xpath("./div[@class='info']/ul/li[@class='title']/a/em/text()").extract_first()
            movie_info = item.xpath(
                "./div[@class='info']/ul/li[@class='title']/a/em/following-sibling::text()").extract_first()
            movie_intro = item.xpath("./div[@class='info']/ul/li[@class='intro']/text()").extract_first()
            movie_date = item.xpath("./div[@class='info']/ul/li/span[@class='date']/text()").extract_first()

            movie = DoubanItem(image_url=image_url, movie_name=movie_name, movie_info=movie_info,
                               movie_intro=movie_intro, movie_date=movie_date)

            yield movie
