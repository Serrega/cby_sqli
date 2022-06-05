#!/usr/bin/env python3
from connect import my_request as req


if __name__ == '__main__':
    url = "http://178.208.95.16/sql_lab/blues"
    cook = dict(
        session='eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2Vyc0xvZ2dlZCI6InJkem9ncyJ9.YnzZMA.c5mcwY9koq-WJE18kKRTNQGbBwI')

    param = dict(go = f'http://178.208.95.16/sql_lab/blues?id={cod}')
    
    response = req.post_request(url, param, cook)
    print('\n', response)    