import abc
import requests


class AbstractBookService(abc.ABC):
    @abc.abstractmethod
    def add(self, title, author, publisher, pages):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, title):
        raise NotImplementedError


class RemoteBookService(AbstractBookService):
    def __init__(self, host):
        self.host = host

    def add(self, title, author, publisher, pages):
        return requests.post(
            f"{self.host}/book",
            json=dict(title=title, author=author, publisher=publisher, pages=pages),
            headers=self._get_auth_header(),
        ).json()

    def get(self, title):
        return requests.get(
            f"{self.host}/book/{title}", headers=self._get_auth_header()
        ).json()

    def _get_auth_header(self, username="test", password="test"):
        response = requests.post(
            f"{self.host}/login", json=dict(username=username, password=password)
        ).json()

        access_token = response["access_token"]

        return {"Authorization": f"Bearer {access_token}"}