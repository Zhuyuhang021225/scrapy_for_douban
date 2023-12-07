# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    image_url = scrapy.Field()
    movie_name = scrapy.Field()
    movie_info = scrapy.Field()
    movie_intro = scrapy.Field()
    movie_date = scrapy.Field()
    user_id = scrapy.Field()
