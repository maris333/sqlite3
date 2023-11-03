import sqlite3


class Database:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS Customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL, surname TEXT NOT NULL, date_joined DATE NOT NULL);"
        self.con.execute(query)

    def add_to_customers(self, name, surname, date_joined):
        query = "INSERT INTO Customers(name, surname, date_joined) VALUES(?, ?, ?)"
        self.con.execute(query, (name, surname, date_joined))

    def preview_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        results = self.con.execute(query).fetchall()
        print(results)

    def delete_from_customers(self, customer_id):
        query = "DELETE FROM Customers WHERE id = ?"
        self.con.execute(query, (customer_id,))

    def update_customer(self, customer_id, name=None, surname=None, date_joined=None):
        query = "UPDATE Customers SET"
        updates = []
        if name:
            updates.append(f"name = '{name}'")
        if surname:
            updates.append(f"surname = '{surname}'")
        if date_joined:
            updates.append(f"date_joined = '{date_joined}'")
        query += ", ".join(updates)
        query += f" WHERE id = {customer_id}"
        self.con.execute(query)

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()


with Database('example2-data') as db:
    db.create_table()
    db.add_to_customers('John', 'Wick', '2000-09-02')
    db.add_to_customers('James', 'Bond', '2002-05-16')
    db.preview_table('Customers')

    db.delete_from_customers(1)
    print("After deletion:")
    db.preview_table('Customers')

    db.update_customer(2, name='Updated Name')
    print("After update:")
    db.preview_table('Customers')
