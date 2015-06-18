# -*- coding: utf-8 -*-
import re
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class FundDetail(object):
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
        'CREATE TABLE if not exists fund_detail(fund_date date,\
          over_price varchar(10),\
          change_percent varchar(10),\
          main_fund varchar(10),\
          main_fund_percent varchar(10),\
          biggest_fund varchar(10),\
          biggest_fund_percent varchar(10),\
          big_fund varchar(10),\
          big_fund_percent varchar(10),\
          middle_fund varchar(10),\
          middle_fund_percent varchar(10),\
          little_fund varchar(10),\
          little_fund_percent varchar(10));',
        ]
        for sql in sql_list:
            tx.execute(sql)

    def insert_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute(
            "insert into fund_detail values (%s%s)"%('\'%s\','*12,'\'%s\'')%tuple(item)
        )

    def handle_error(self, e):
        log.err(e)