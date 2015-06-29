# -*- coding: utf-8 -*-
import re
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
import time
import MySQLdb
import MySQLdb.cursors


class StockPipeline(object):
    def process_item(self, item, spider):
        return item

class ListedCompanyPipeline(object):
    """docstring for MySQLstor"""
    def __init__(self):
        '''
        CREATE DATABASE `stock` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
        '''
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'stock',
            user = 'root',
            passwd = 'root',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
        self.create_tables()

    def create_tables(self):
        query = self.dbpool.runInteraction(self._execute_create_table_sql)
        query.addErrback(self.handle_error)

    def _execute_create_table_sql(self,tx):
        sql_list = [
        'CREATE TABLE if not exists listed_company(name varchar(50),symbol varchar(10),code varchar(10) primary key);',
        ]
        for sql in sql_list:
            tx.execute(sql)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute(
            "insert into listed_company (name, symbol, code)\
            values ('%s', '%s', '%s')" % (item['name'],item['symbol'],item['code'])
        )

    def handle_error(self, e):
        log.err(e)