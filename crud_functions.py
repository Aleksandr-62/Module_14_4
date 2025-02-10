import sqlite3

def initiate_db():
    connection = sqlite3.connect('product.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    img_name TEXT
    )    
    ''')
    connection.commit()
    connection.close()


def set_product(title,description,price,img_name):
    connection = sqlite3.connect('product.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Products (title,description,price, img_name) VALUES (?,?,?,?)",
                   (f'{title}', f'{description}', f'{price}',f'{img_name}'))
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('product.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    total = cursor.fetchall()
    connection.close()
    return total

# initiate_db()
# set_product("Product_1",'Красота',100, "1.jpg")
# set_product("Product_2",'Иммунитет',200, "2.jpg")
# set_product("Product_3",'Здоровье',300, "3.jpg")
# set_product("Product_4",'Лишний вес',400, "4.jpg")