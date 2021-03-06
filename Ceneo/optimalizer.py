import sqlite3
import itertools
import sys
import json
import os

class Product:
    delivery_price = float('NaN')

    def __init__(self, row):
        self.object_name = row[0]
        self.price = row[1]
        self.delivery_info = row[2]
        self.website_link = row[3]
        self.shop_name = row[4]
        self.shop_rating = row[5]
        self.shop_reviews_number = row[6]
        self.quantity = row[7]
        self.calculate_delivery_price()                
        self.object_name = self.object_name.replace('"', ' cali')
        self.object_name = self.object_name.replace("'", ' cali')

    def calculate_delivery_price(self):
        if "Darmowa" in self.delivery_info:
            self.delivery_price = 0
        elif "szczegóły" not in self.delivery_info:
            tmp = ""
            for i in range(len("Z wysyłką od\r\n"),
                           len(self.delivery_info)):
                if self.delivery_info[i] in "0123456789,":
                    tmp += self.delivery_info[i]
            tmp = float(tmp.replace(",", "."))
            self.delivery_price = round(tmp - self.price, 2)


def database_to_object(path):
    con = sqlite3.connect(path)
    obj_list = []
    sql_request = """   SELECT * FROM products 
                                WHERE shop_reviews_number > 20 
                                AND delivery_info NOT LIKE 'szczegóły dostawy' 
                            ORDER BY price;     """
    for row in con.execute(sql_request):
    	obj_list.append(Product(row))
    return obj_list


def list_of_products(database_name, prefix=""):
    product_list = []
    for i in database_name:
        dto = database_to_object(prefix + i)
        if len(dto) >= 3:
            product_list.append(dto)
    return product_list


def find_optimal(product_list):
    possibility = []
    for sequence in itertools.product(*product_list):
        try:
            possibility.append(sequence)
        except MemoryError as error:
             print(str(error))
             pass

    final_list = []
    for product in possibility:
        del_pri = {}
        final_price = 0
        for i in product:
            if i.shop_name not in del_pri:
                del_pri[i.shop_name] = i.delivery_price
            elif del_pri[i.shop_name] < i.delivery_price:
                del_pri[i.shop_name] = i.delivery_price
            final_price += i.price * i.quantity
        final_price += sum(del_pri.values())
        final_list.append([product, round(final_price, 2)])

    final_list = sorted(final_list, key=lambda row: row[1])
    return final_list

def read_db_names():
	input_db = []
	for i in os.listdir("tmp"):
		if i[-3:] == ".db" and "products_from_search_page" not in i:
			input_db.append(i)
	return input_db

def result_to_dict(final_list):
    total_list=[]
    for i in range(min(3,len(final_list))):
        tmp_external_dict = {}
        tmp_list = []
        save_shop = []
        for j in final_list[i][0]:
            tmp_dictionary = {}
            if j.shop_name in save_shop:
                tmp_dictionary["delivery"] = 0
            else: 
                tmp_dictionary["delivery"] = j.delivery_price
            save_shop.append(j.shop_name)
            tmp_dictionary["name"] = j.object_name
            tmp_dictionary["price"] = j.price
            tmp_dictionary["link"] = j.website_link
            tmp_dictionary["store"] = j.shop_name
            tmp_dictionary["quantity"] = j.quantity
            tmp_list.append(tmp_dictionary)
        tmp_external_dict["products"] = tmp_list
        tmp_external_dict["costs"] = final_list[i][1]
        total_list.append(tmp_external_dict)
    output_data = {}
    output_data["sets"] = total_list
    return output_data

def save_output(output_data, path_to_output):
    with open(path_to_output, "w+") as json_file:
        json.dump(output_data, json_file)

def main():
	input_db = read_db_names()
	product_list = list_of_products(input_db, 'tmp\\')
	final_list = find_optimal(product_list)
	
	output_data = result_to_dict(final_list)
	save_output(output_data, "tmp\\output_data.txt")


if __name__ == '__main__':
	main()