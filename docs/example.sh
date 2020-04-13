#!/bin/bash
# coding=utf-8

"""
codecov|https://codecov.io/gh/Jewel591/CheckXSS
"""

python3 ../checkxss.py -u "http://demo.testfire.net/search.jsp?query=windws" --ua="checkxss" --cookie="JSESSIONID=9B7ADB9D3DB7FC018F9FE641612558BE" -p query
