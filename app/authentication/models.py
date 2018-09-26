class User():
    def __init__(self, email, username, password, isAdmin):
        self._email = email
        self._username = username
        self._password = password
        self._isAdmin = isAdmin

    @property
    def email(self):
        return self._email

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def isAdmin(self):
        return self._isAdmin
