import pyodbc

class DatabaseDriver:
    def __init__(self):
        try:
            self.Conn = pyodbc.connect("Driver={SQL Server};" +
                                       "Server=DESKTOP-96QO9A0\\SQLEXPRESS;" +
                                       "Database=phishsheild;" +
                                       "Trusted_Connection=True;")
        except pyodbc.Error as ex:
            print("Connection Failed : ", ex)

    def StoreHash(self, hash):
        # Create a cursor from the connection
        cursor = self.Conn.cursor()
        # Define the SQL query to insert data
        insert_query = "INSERT INTO hashtable (hashes) VALUES (?)"
        cursor.execute(insert_query, hash)
        self.Conn.commit()
        # print("Hash value inserted successfully.")
        # Close the cursor
        cursor.close()

    def FetchHash(self):
        # Create a cursor from the connection
        cursor = self.Conn.cursor()
        fetch_query = "SELECT hashes FROM hashtable"
        cursor.execute(fetch_query)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Extract the hash values into a list
        hash_list = [row.hashes for row in rows]
        cursor.close()
        return hash_list

    def StoreURL(self, url):
        # Create a cursor from the connection
        cursor = self.Conn.cursor()
        # Define the SQL query to insert data
        insert_query = "INSERT INTO urltable (urls) VALUES (?)"
        cursor.execute(insert_query, url)
        self.Conn.commit()
        # print("Hash value inserted successfully.")
        # Close the cursor
        cursor.close()

    def FetchURL(self):
        # Create a cursor from the connection
        cursor = self.Conn.cursor()
        fetch_query = "SELECT urls FROM urltable"
        cursor.execute(fetch_query)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Extract the hash values into a list
        url_list = [row.urls for row in rows]
        cursor.close()
        return url_list

    def Check_User_Existence(self, email):
        # Create a cursor from the connection
        cursor = self.Conn.cursor()
        fetch_query = "SELECT * FROM euser WHERE email = ?"
        cursor.execute(fetch_query, email)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()
        if len(rows) > 0:
            return True
        return False

    def Check_User_Reputation(self, email):
        # Create a cursor from the connection
        cursor = self.Conn.cursor()
        fetch_query = "SELECT * FROM euser WHERE email = ?"
        cursor.execute(fetch_query, email)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()
        reputation = rows[0].rep
        return reputation

    def Create_EUser(self, email):
        # Create a cursor from the connection
        cursor = self.Conn.cursor()
        # Define the SQL query to insert data
        insert_query = "INSERT INTO euser (email, rep) VALUES (?, 100)"
        cursor.execute(insert_query, email)
        self.Conn.commit()
        print("User inserted successfully.")
        # Close the cursor
        cursor.close()