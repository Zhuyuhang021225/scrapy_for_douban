# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class DoubanPipeline:
    def open_spider(self, spider):
        source = spider.crawler.settings.get('source')
        user_id = spider.crawler.settings.get('user_id')
        if source == 'wish':
            self.fp1 = open(f"./jsons/{user_id}_wish.json", "w", encoding="utf-8")
        if source == 'collect':
            self.fp2 = open(f"./jsons/{user_id}_collect.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        source = spider.crawler.settings.get('source')
        if source == 'wish':
            self.fp1.write(str(item))
        if source == 'collect':
            self.fp2.write(str(item))
        return item

    def close_spider(self, spider):
        source = spider.crawler.settings.get('source')
        if source == 'wish':
            self.fp1.close()
        if source == 'collect':
            self.fp2.close()


class MysqlPipeline:
    def get_conn(self):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="spider01",
            user="root",
            password="123456"
        )

    def open_spider(self, spider):
        source = spider.crawler.settings.get('source')
        self.get_conn()
        if source == 'wish':
            self.cursor1 = self.conn.cursor()
        if source == 'collect':
            self.cursor2 = self.conn.cursor()

    def process_item(self, item, spider):
        source = spider.crawler.settings.get('source')
        user_id = spider.crawler.settings.get('user_id')
        if source == 'wish':
            sql = 'insert into wish(name,date,info,intro,url,user_id) values ("{}","{}","{}","{}","{}","{}")'.format(
                item['movie_name'], item['movie_date'], item['movie_info'], item['movie_intro'], item['image_url'],
                user_id)
            self.cursor1.execute(sql)
            self.conn.commit()
        if source == 'collect':
            sql = 'insert into collect(name,date,info,intro,url,user_id) values ("{}","{}","{}","{}","{}","{}")'.format(
                item['movie_name'], item['movie_date'], item['movie_info'], item['movie_intro'], item['image_url'],
                user_id)
            self.cursor2.execute(sql)
            self.conn.commit()
        return item

    def close_spider(self, spider):
        source = spider.crawler.settings.get('source')
        if source == 'wish':
            self.cursor1.close()
        if source == 'collect':
            self.cursor2.close()
        self.conn.close()
