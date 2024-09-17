from DB.DatabaseDriver import DatabaseDriver

def test_connection():
    db_driver = DatabaseDriver()
    if db_driver.Conn is not None:
        print("Connection established successfully.")
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    test_connection()
