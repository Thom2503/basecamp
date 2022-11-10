class PasswordManager:
    """
    Class to organize passwords like a password manager
    """

    def __init__(self):
        self.old_passwords: list = []

    def get_password(self) -> str:
        return self.old_passwords[-1]

    def set_password(self, password):
        if password not in self.old_passwords:
            self.old_passwords.append(password)

    def is_correct(self, password) -> bool:
        return password == self.get_password()


def main():
    password_manager = PasswordManager()

    password_manager.set_password("test")
    print(password_manager.get_password())
    print(password_manager.is_correct("Test"))
    print(password_manager.is_correct("test"))


if __name__ == "__main__":
    main()
