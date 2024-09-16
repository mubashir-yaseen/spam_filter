from DB.DatabaseDriver import DatabaseDriver


class Reputation_Checker:
    def __init__(self):
        pass

    def Check_Reputation(self, email):
        driver = DatabaseDriver()
        flag = driver.Check_User_Existence(email)
        rep = 0
        if flag == False:
            driver.Create_EUser(email)
        else:
            rep = driver.Check_User_Reputation(email)

        print(rep)
        return rep


# Main Code

reputationChecker = Reputation_Checker()
rep = reputationChecker.Check_Reputation("hello@gmail.com")

if rep < 50:
    print("Spam Email")
elif rep < 80:
    print("Suspected Spam")
else:
    print("Not Spam")