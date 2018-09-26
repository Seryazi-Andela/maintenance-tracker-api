class UserRequest():
    def __init__(self, username=None, header=None, details=None, approved=False, resolved=False):
        self._username = username
        self._header = header
        self._details = details
        self._approved = approved
        self._resolved = resolved

    @property
    def username(self):
        return self._username

    @property
    def header(self):
        return self._header

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, details):
        self._details = details

    @property
    def approved(self):
        return self._approved

    @approved.setter
    def approved(self, approved):
        self._approved = approved

    @property
    def resolved(self):
        return self._resolved

    @resolved.setter
    def resolved(self, resolved):
        self._resolved = resolved
