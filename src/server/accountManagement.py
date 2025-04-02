import sqlite3
import database_manager
from argon2 import PasswordHasher
ph = PasswordHasher()

class Account:
    def __init__(self, username, email, password, personal_details=None):
        self.username = username
        self.email = email
        self.password = password
        self.personal_details = personal_details or {}

    @staticmethod
    def from_db_row(row):
        return Account(
            id=row['id'],
            username=row['username'],
            email=row['email']
        )


class AccountManager:
    def __init__(self):
        self.logged_in_user = None

    def login(self, username, password):
        query = "SELECT * FROM accounts WHERE username = ?"
        result = database_manager.get_user_info(username)
        if result :
            try :
                ph.verify(result['password'], password)
            except:
                print("Invalid username or password.")
                return False
            self.logged_in_user = Account.from_db_row(result)
            return True
        print("Invalid username or password.")
        return False

    def logout(self):
        self.logged_in_user = None

    def change_password(self, old_password, new_password):
        if self.logged_in_user:
            if self.logged_in_user.password == old_password:
                query = "UPDATE accounts SET password = ? WHERE username = ?"
                self.db_manager.execute(query, (new_password, self.logged_in_user.username))
                self.logged_in_user.password = new_password
                print("Password updated successfully.")
                return True
            else:
                print("Old password is incorrect.")
        else:
            print("No user is logged in.")
        return False

    def delete_account(self):
        if self.logged_in_user:
            username = self.logged_in_user.username
            del self.accounts[username]
            self.logged_in_user = None
            print(f"Account '{username}' deleted successfully.")
            return True
        else:
            print("No user is logged in.")
        return False

    def forgot_password(self, username, email):
        if username in self.accounts:
            account = self.accounts[username]
            if account.email == email:
                print(f"Password reset link sent to {email}.")
                return True
            else:
                print("Email does not match our records.")
        else:
            print("Account not found.")
        return False