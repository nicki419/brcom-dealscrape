"""Link: https://www.blu-ray.com/deals/?sortby=time&category=2kbluray&retailerid=1&covers=10
Amazon: ID 1
Walmart: ID 8
BestBuy: ID 2"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from collections import OrderedDict
import mysql.connector
from dotenv import dotenv_values
from re import sub
from decimal import Decimal

def get_deals(url, country):
    response = requests.get(url, cookies={"deallink": "bluray", "country": country})
    if(str(response) == "<Response [200]>"):
        soup = BeautifulSoup(response.text, "html.parser")
        
    else:
        return False
    
    items = OrderedDict()
    for i in soup.findAll("center"):
        if("<a alt=" in str(i) and "blu-ray.com" in str(i) and "select" not in str(i) and "option" not in str(i)):
            name = i.contents[0]["title"]
            link_info = i.contents[0]["href"]
            try:
                thumb = i.contents[0].findAll("img")[0]["src"]
            except:
                thumb = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Icon-round-Question_mark.svg/200px-Icon-round-Question_mark.svg.png"
            link_buy = i.contents[2].findAll("a")[0]["href"]
            price = i.contents[2].findAll("a")[0].contents[0]
            old_price = i.contents[2].findAll("strike")[0].contents[0]
            items[name] = {
                "name": name,
                "link_info": link_info,
                "link_buy": link_buy,
                "thumb": thumb,
                "price": price,
                "old_price": old_price}
            
    return(items)
                   
def store_to_db(name, deal_dict):
    returns = OrderedDict()
    
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
        cursor.execute(str("alter table " + name + " modify name varchar(1024) character set utf8mb4 collate 'utf8mb4_general_ci'"))
        print("Created table '"+name+"'.")
    
    #Grab Current DB Entries
    cursor.execute(str("SELECT * FROM "+name))
    result = cursor.fetchall()
    
    if(result == []): #Check if Entries Empty
        for i in deal_dict:
            cursor.execute(str("INSERT INTO "+name+" (name, link_info, link_buy, thumb, price, old_price, date_added) VALUES ('"+deal_dict[i]["name"].replace("'", "''")+"', '"+deal_dict[i]["link_info"]+"', '"+deal_dict[i]["link_buy"]+"', '"+deal_dict[i]["thumb"]+"', '"+deal_dict[i]["price"]+"', '"+deal_dict[i]["old_price"]+"', '"+str(int(time.time()))+"')"))
            print(str("Added New Deal: "+deal_dict[i]["name"]))
            returns[i] = {
                "name": deal_dict[i]["name"],
                "link_info": deal_dict[i]["link_info"],
                "link_buy": deal_dict[i]["link_buy"],
                "thumb": deal_dict[i]["thumb"],
                "price": deal_dict[i]["price"],
                "old_price": deal_dict[i]["old_price"]}
        
        db.commit()
        return returns
        
    else:
        for i in result:
            if int(time.time())-2592000 > i[7]: #Delete Entries older than 30 days
                cursor.execute(str("DELETE FROM "+name+" WHERE id="+str(i[0])))
                print("Deleted Deal (Older 30d): "+i[1])
                
        for i in deal_dict:
            cursor.execute(str("SELECT * FROM "+name+" WHERE link_info='"+deal_dict[i]["link_info"]+"'"))
            comp_res = cursor.fetchall()
            
            if(comp_res != []): #Check if deal_dict entry is already in DB
                cursor.execute(str("SELECT * FROM "+name+" WHERE link_info='"+deal_dict[i]["link_info"]+"' LIMIT 1")) #Grab Entry from DB
                temp_result = cursor.fetchall()
                
                try:
                    if Decimal(sub(r'[^\d.]', '', deal_dict[i]["price"])) != Decimal(sub(r'[^\d.]', '', temp_result[0][5])): #Check if deal_dict price is different
                        cursor.execute(str("DELETE FROM "+name+" WHERE id="+str(temp_result[0][0])))
                        cursor.execute(str("INSERT INTO "+name+" (name, link_info, link_buy, thumb, price, old_price, date_added) VALUES ('"+deal_dict[i]["name"].replace("'", "''")+"', '"+deal_dict[i]["link_info"]+"', '"+deal_dict[i]["link_buy"]+"', '"+deal_dict[i]["thumb"]+"', '"+deal_dict[i]["price"]+"', '"+deal_dict[i]["old_price"]+"', '"+str(int(time.time()))+"')"))
                        print("Deal Updated for: "+str(i))
                        returns[i] = {
                            "name": deal_dict[i]["name"],
                            "link_info": deal_dict[i]["link_info"],
                            "link_buy": deal_dict[i]["link_buy"],
                            "thumb": deal_dict[i]["thumb"],
                            "price": deal_dict[i]["price"],
                            "old_price": deal_dict[i]["old_price"]}
                except:
                    print(str(temp_result))
                    print("Exception in Price Comparison - Deleting DB Entry")
                    
                    
            else:
                cursor.execute(str("INSERT INTO "+name+" (name, link_info, link_buy, thumb, price, old_price, date_added) VALUES ('"+deal_dict[i]["name"].replace("'", "''")+"', '"+deal_dict[i]["link_info"]+"', '"+deal_dict[i]["link_buy"]+"', '"+deal_dict[i]["thumb"]+"', '"+deal_dict[i]["price"]+"', '"+deal_dict[i]["old_price"]+"', '"+str(int(time.time()))+"')"))
                print("Added New Deal: "+str(i))
                returns[i] = {
                    "name": deal_dict[i]["name"],
                    "link_info": deal_dict[i]["link_info"],
                    "link_buy": deal_dict[i]["link_buy"],
                    "thumb": deal_dict[i]["thumb"],
                    "price": deal_dict[i]["price"],
                    "old_price": deal_dict[i]["old_price"]}
            
        db.commit()
        return returns
