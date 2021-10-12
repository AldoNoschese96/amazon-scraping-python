import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
import pprint 

url = 'http://amazon.it/'
search_terms = "mobile gaming"
isPrintingOnShell = "n"
restart='n'

def check_last_index_db(db):
    key_to_return = "0"
    for key in db:
        key_to_return = key
    return key_to_return

def buld_url_to_product(node):
    if node is not None:
        return f'{url + node.attrs["href"]}'
    else:
        return None

def check_str(value):
    if type(value) is str:
        return True
    else:
        return False

def check_node_isNot_None(node):
    if node is not None:
        return node.text
    else:
        return None

def make_dict_to_write(array , terms):
    report_dict = {}
    products_list = []
    for el in array:
        products_list.append(el)
    report_dict["report_date"] = f'{date.today()}'
    report_dict["search_terms"] = terms
    report_dict["products"] = products_list
    return report_dict
    
def build_element_to_write(element):
    product_dict = {}
    price = check_node_isNot_None(element.find(f"span" , class_="a-price-whole"))
    description = check_node_isNot_None(element.find("span" , class_="a-size-base-plus"))
    url = buld_url_to_product(element.find("a" , class_="a-link-normal"))
    if check_str(price) == True and check_str(description) == True:
        product_dict["product_description"] = description
        product_dict["product_price"] = price
        product_dict["product_url"] = url
        return product_dict

def get_json_db():
    with open('./history/report.json') as json_file:
        try:
            data = json.load(json_file)
            return data
        except:
            raise TypeError("Error While trying to read report")

def override_db_handler(last_index , json_db , dict_db):
    current_index = str(int(last_index) + 1)
    json_db[current_index] = dict_db
    return json_db 
    
def write_document(dict_db):
    last_index = check_last_index_db(get_json_db())
    override_db = override_db_handler(last_index , get_json_db() , dict_db)
    if isPrintingOnShell == True:
        pprint.pprint(override_db)
    with open("./history/report.json" , "w") as f:
        try:
            json.dump(override_db, f)
        except:
            raise TypeError("Error While trying to write report")

def user_input_handler():
    global search_terms 
    global isPrintingOnShell 
    search_terms = input("Inserisci un termine di ricerca : ")
    isPrintingOnShell = input("Vuoi Vedere il risultato della ricerca nella shell (y/n) ? ")
    if isPrintingOnShell == 'y':
        isPrintingOnShell = True
    else:
        isPrintingOnShell = False

def start_scraping(url , terms):
    user_input_handler()
    print(f'Reaching {url} wait please..')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(executable_path=r"./driver/chromedriver" ,options=options)
    driver.get(url)
    time.sleep(5)
    print(f'Searching << {search_terms} >> in {url} wait please..')
    driver.find_element_by_id("twotabsearchtextbox").send_keys(terms)
    driver.find_element_by_id("nav-search-bar-form").submit()
    time.sleep(5)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    products_array = []
    for tag in soup.find_all("div" , class_="s-result-item"):
        dict_to_append = build_element_to_write(tag)
        if type(dict_to_append) is dict:
            products_array.append(dict_to_append)
    write_document(make_dict_to_write(products_array , terms))
    driver.close()
    print(f'Report Generated !')
        

start_scraping(url , search_terms)









