class Account:
    def __init__(self, username, email, password, personal_details=None):
        self.username = username
        self.email = email
        self.password = password
        self.personal_details = personal_details or {}

    def update_password(self, new_password):
        self.password = new_password

    def update_personal_details(self, new_details):
        self.personal_details.update(new_details)


class AccountManager:
    def __init__(self):
        self.logged_in_user = None
        self.accounts = {}

    def login(self, username, password):
        if username in self.accounts:
            account = self.accounts[username]
            if account.password == password:
                self.logged_in_user = account
                return True
            else:
                print("Invalid password.")
        else:
            print("Account not found.")
        return False

    def logout(self):
        self.logged_in_user = None

    def change_password(self, old_password, new_password):
        if self.logged_in_user:
            if self.logged_in_user.password == old_password:
                self.logged_in_user.update_password(new_password)
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