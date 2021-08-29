"""
Link: https://www.blu-ray.com/deals/?sortby=time&category=2kbluray&retailerid=1&covers=10
Amazon: ID 1
Walmart: ID 8
BestBuy: ID 2
"""

#get_info
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from collections import OrderedDict

#create_table
import mysql.connector
from dotenv import dotenv_values

def get_deals(url):
    response = requests.get(url, cookies={"deallink": "bluray"})
    if(str(response) == "<Response [200]>"):
        soup = BeautifulSoup(response.text, "html.parser")
    else:
        return False
    
    items = OrderedDict()
    
    for i in soup.findAll("center"):
        
        if("<a alt=" in str(i) and "blu-ray.com" in str(i) and "select" not in str(i) and "option" not in str(i)):
            
            name = i.contents[0]["title"]
            link_info = i.contents[0]["href"]
            thumb = i.contents[0].findAll("img")[0]["src"]
            link_buy = i.contents[2].findAll("a")[0]["href"]
            price = i.contents[2].findAll("a")[0].contents[0]
            old_price = i.contents[2].findAll("strike")[0].contents[0]
            
            items[name] = {
                "name": name,
                "link_info": link_info,
                "link_buy": link_buy,
                "thumb": thumb,
                "price": price,
                "old_price": old_price
            }
            
    return(items)
                
    
    
def store_to_db(name, deal_dict):
    DB_config = dotenv_values("moviedeals.env")
    
    db = mysql.connector.connect(
        host=DB_config["DB_HOST"],
        user=DB_config["DB_USER"],
        password=DB_config["DB_PASS"],
        database=DB_config["DB_DATABASE"],
        port=DB_config["DB_PORT"]
    )
    
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(name.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        print("Found table '"+name+"'.")
    else:
        cursor.execute(str("CREATE TABLE " + name + " (id MEDIUMINT NOT NULL AUTO_INCREMENT, name VARCHAR(1024), link_info VARCHAR(512), link_buy VARCHAR(512), thumb VARCHAR(512), price VARCHAR(64), old_price VARCHAR(64), date_added int(11), PRIMARY KEY (id))"))
        print("Created table '"+name+"'.")
        cursor.execute(str("alter table " + name + " modify name varchar(1024) character set utf8mb4 collate 'utf8mb4_general_ci'"))
        
    for i in deal_dict:
        
        cursor.execute(str("INSERT INTO "+name+" (name, link_info, link_buy, thumb, price, old_price, date_added) VALUES ('"+deal_dict[i]["name"].replace("'", "''")+"', '"+deal_dict[i]["link_info"]+"', '"+deal_dict[i]["link_buy"]+"', '"+deal_dict[i]["thumb"]+"', '"+deal_dict[i]["price"]+"', '"+deal_dict[i]["old_price"]+"', '"+str(int(time.time()))+"')"))
        
        print(str("Insterted '"+deal_dict[i]["name"]+"' into Database."))
    db.commit()

    
#deals = get_deals("https://www.blu-ray.com/deals/?sortby=time&category=4kbluray&retailerid=1&covers=10")
#store_to_db("test", deals)
    


