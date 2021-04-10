#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/3/20 9:36'

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


def main():
    app.run()


if __name__ == '__main__':
    main()
