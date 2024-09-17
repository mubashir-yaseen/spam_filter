from DB.DatabaseDriver import DatabaseDriver

def test_db_operations():
    db_driver = DatabaseDriver()

    # Test inserting and fetching hashes
    db_driver.StoreHash("samplehash123")
    print("Hashes in database:", db_driver.FetchHash())

    # Test inserting and fetching URLs
    db_driver.StoreURL("http://example.com")
    print("URLs in database:", db_driver.FetchURL())

    # Test user existence
    email = "testuser@example.com"
    if not db_driver.Check_User_Existence(email):
        db_driver.Create_EUser(email)
    print("User reputation:", db_driver.Check_User_Reputation(email))

if __name__ == "__main__":
    test_db_operations()
