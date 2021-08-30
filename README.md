# brcom-dealscrape
A Python 3 Webscraping module that gets deals from Blu-ray.com and stores them to a MariaDB table

**Required Modules**: requests, urllib.request, time, beautifulsoup4, collections, mysql.connector, dotenv

**Modules and Usage**:
get_deals("URL") takes a deal page URL, returns a dictionary with Title, Thumbnail Link, Blu-ray.com link, vendor link, price, old price

store_to_db("name", dict):
requires moviedeals.env to be filled out. Requires MySQL Database (tested with MariaDB) and user with all privileges on said database.
"name" refers to the table name. Should said table already exist, it'll store the dictionary items in the table. Should it not exist, it will create it first. 

Checks for duplicate entries in the database, and, if found, checks for an updated price to the item. If found, the database entry will be deleted, and the deal added anew.
Automatically Deletes Entries older than 30 Days from the Database.

copy the .py file in your project's directory, as well as the moviedeals.env file.

example usage: 
```python
import importlib

ds = importlib.import_module("dealscrape")

deals = ds.get_deals("https://www.blu-ray.com/deals/?sortby=time&category=4kbluray&retailerid=1&covers=10", "us")
ds.store_to_db("4K_Deals", deals)
```

example stdout:
```
Created table '4K_Deals'.
Added New Deal: 'Shutter Island 4K (Blu-ray)
Added New Deal: 'A Quiet Place Part II 4K (Blu-ray)
Added New Deal: 'Two Evil Eyes 4K (Blu-ray)
Added New Deal: 'Carlito's Way 4K (Blu-ray)
```
example database:
```
MariaDB [moviedeals]> select * from 4K_Deals limit 10;
+----+------------------------------------------------------+----------------------------------------------------------------------------------------+-----------------------------------------------------------------------+------------------------------------------------------------------+--------+-----------+------------+
| id | name                                                 | link_info                                                                              | link_buy                                                              | thumb                                                            | price  | old_price | date_added |
+----+------------------------------------------------------+----------------------------------------------------------------------------------------+-----------------------------------------------------------------------+------------------------------------------------------------------+--------+-----------+------------+
|  1 | Shutter Island 4K (Blu-ray)                          | https://www.blu-ray.com/movies/Shutter-Island-4K-Blu-ray/228674/                       | https://www.blu-ray.com/link/click.php?p=1064150&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/228674_medium.jpg | $19.19 | $19.39    | 1630244950 |
|  2 | A Quiet Place Part II 4K (Blu-ray)                   | https://www.blu-ray.com/movies/A-Quiet-Place-Part-II-4K-Blu-ray/265100/                | https://www.blu-ray.com/link/click.php?p=1263998&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/265100_medium.jpg | $24.51 | $24.95    | 1630244950 |
|  3 | Two Evil Eyes 4K (Blu-ray)                           | https://www.blu-ray.com/movies/Two-Evil-Eyes-4K-Blu-ray/289612/                        | https://www.blu-ray.com/link/click.php?p=1431203&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/289612_medium.jpg | $33.02 | $44.99    | 1630244950 |
|  4 | Carlito's Way 4K (Blu-ray)                           | https://www.blu-ray.com/movies/Carlitos-Way-4K-Blu-ray/296947/                         | https://www.blu-ray.com/link/click.php?p=1462080&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/296947_medium.jpg | $19.99 | $29.98    | 1630244950 |
|  5 | Beverly Hills Cop 4K (Blu-ray)                       | https://www.blu-ray.com/movies/Beverly-Hills-Cop-4K-Blu-ray/277487/                    | https://www.blu-ray.com/link/click.php?p=1355630&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/277487_medium.jpg | $16.44 | $16.67    | 1630244950 |
|  6 | The Addams Family 4K - with More Mamushka! (Blu-ray) | https://www.blu-ray.com/movies/The-Addams-Family-4K-with-More-Mamushka-Blu-ray/293203/ | https://www.blu-ray.com/link/click.php?p=1446783&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/293203_medium.jpg | $23.99 | $25.99    | 1630244950 |
|  7 | Dead & Buried 4K (Blu-ray)                           | https://www.blu-ray.com/movies/Dead-and-Buried-4K-Blu-ray/288798/                      | https://www.blu-ray.com/link/click.php?p=1427349&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/288798_medium.jpg | $41.99 | $42.49    | 1630244950 |
|  8 | The Outpost (Blu-ray)                                | https://www.blu-ray.com/movies/The-Outpost-Blu-ray/286686/                             | https://www.blu-ray.com/link/click.php?p=1415562&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/286686_medium.jpg | $19.32 | $19.52    | 1630244950 |
|  9 | How to Train Your Dragon 4K (Blu-ray)                | https://www.blu-ray.com/movies/How-to-Train-Your-Dragon-4K-Blu-ray/220562/             | https://www.blu-ray.com/link/click.php?p=962661&retailerid=1&tid=074  | https://images.static-bluray.com/movies/covers/220562_medium.jpg | $15.72 | $19.98    | 1630244950 |
| 10 | Deep Red 4K (Blu-ray)                                | https://www.blu-ray.com/movies/Deep-Red-4K-Blu-ray/291114/                             | https://www.blu-ray.com/link/click.php?p=1437606&retailerid=1&tid=074 | https://images.static-bluray.com/movies/covers/291114_medium.jpg | $42.99 | $53.06    | 1630244950 |
+----+------------------------------------------------------+----------------------------------------------------------------------------------------+-----------------------------------------------------------------------+------------------------------------------------------------------+--------+-----------+------------+
```
