import pyodbc

class DatabaseDriver:
    def __init__(self):
        try:
            self.Conn = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=DESKTOP-6UPONFK\\SQLEXPRESS;"  # Ensure this matches your server name
                "Database=phishsheild;"  # Ensure this matches your database name
                "Trusted_Connection=True;"
            )
        except pyodbc.Error as ex:
            print("Connection Failed: ", ex)
            self.Conn = None

    def StoreHash(self, hash):
        if self.Conn is None:
            print("No connection to the database.")
            return
        cursor = self.Conn.cursor()
        insert_query = "INSERT INTO hashtable (hashes) VALUES (?)"
        cursor.execute(insert_query, hash)
        self.Conn.commit()
        cursor.close()

    def FetchHash(self):
        if self.Conn is None:
            print("No connection to the database.")
            return []
        cursor = self.Conn.cursor()
        fetch_query = "SELECT hashes FROM hashtable"
        cursor.execute(fetch_query)
        rows = cursor.fetchall()
        hash_list = [row.hashes for row in rows]
        cursor.close()
        return hash_list

    def StoreURL(self, url):
        if self.Conn is None:
            print("No connection to the database.")
            return
        cursor = self.Conn.cursor()
        insert_query = "INSERT INTO urltable (urls) VALUES (?)"
        cursor.execute(insert_query, url)
        self.Conn.commit()
        cursor.close()

    def FetchURL(self):
        if self.Conn is None:
            print("No connection to the database.")
            return []
        cursor = self.Conn.cursor()
        fetch_query = "SELECT urls FROM urltable"
        cursor.execute(fetch_query)
        rows = cursor.fetchall()
        url_list = [row.urls for row in rows]
        cursor.close()
        return url_list

    def Check_User_Existence(self, email):
        if self.Conn is None:
            print("No connection to the database.")
            return False
        cursor = self.Conn.cursor()
        fetch_query = "SELECT * FROM euser WHERE email = ?"
        cursor.execute(fetch_query, email)
        rows = cursor.fetchall()
        return len(rows) > 0

    def Check_User_Reputation(self, email):
        if self.Conn is None:
            print("No connection to the database.")
            return None
        cursor = self.Conn.cursor()
        fetch_query = "SELECT rep FROM euser WHERE email = ?"
        cursor.execute(fetch_query, email)
        rows = cursor.fetchall()
        return rows[0].rep if rows else None

    def Create_EUser(self, email):
        if self.Conn is None:
            print("No connection to the database.")
            return
        cursor = self.Conn.cursor()
        insert_query = "INSERT INTO euser (email, rep) VALUES (?, 100)"
        cursor.execute(insert_query, email)
        self.Conn.commit()
        print("User inserted successfully.")
        cursor.close()
