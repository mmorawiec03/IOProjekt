import sqlite3
import sys
import json
import os

number_of_used_links = 0
def get_row(product_number):
    path = r'..\..\tmp\products_from_search_page_' + product_number + '.db'
    conn = sqlite3.connect(path)
    curr = conn.cursor()
    curr.execute("""SELECT count(*) FROM products order by number_of_shops DESC, price;""",())
    number_of_rows = curr.fetchone()
    curr.execute("""SELECT website_link FROM products order by number_of_shops DESC, price;""", (
    ))
    websites_links = curr.fetchmany(int(number_of_rows[0]))
    try:
        str = ''.join(websites_links[number_of_used_links])
    except IndexError:
        str = ''
    return str

def check(product_number):
    path = '../../tmp'
    with open(os.path.join(path, "input_data.txt")) as json_file:
        data = json.load(json_file)
        info = data['products'][product_number]
        reputation = info['reputation']
        name = info['name']
    name_database = name + ".db"
    path = r'..\..\tmp\\' + name_database
    conn = sqlite3.connect(path)
    curr = conn.cursor()
    curr.execute("""SELECT count(*) FROM products where shop_rating > ? and shop_reviews_number > 20;""", (
        [reputation]
    ))
    result = int(curr.fetchone()[0])
    return result

def add_next_link():
    global number_of_used_links
    number_of_used_links = number_of_used_links + 1