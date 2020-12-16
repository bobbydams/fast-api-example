import abc
from datetime import datetime

from apps.api.domain import model
from apps.api.domain.exceptions import BookNotFound


class AbstractBookRepository(abc.ABC):
    def add(self, book: model.Book):
        self._add(book)

    def delete(self, title: str):
        self._delete(title)

    def get(self, title) -> model.Book:
        return self._get(title)

    def update(self, book: model.Book):
        return self._update(book)

    @abc.abstractmethod
    def _add(self, book: model.Book):
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, title: str):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, title: str) -> model.Book:
        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, book: model.Book):
        raise NotImplementedError


class SqlAlchemyBookRepository(AbstractBookRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, book):
        book.created_at = datetime.now()
        book.updated_at = datetime.now()
        self.session.add(book)

    def _delete(self, title):
        self.session.query(model.Book).filter_by(title=title).delete()

    def _get(self, title):
        return self.session.query(model.Book).filter_by(title=title).scalar()

    def _update(self, book):
        book.updated_at = datetime.now()
        self.session.query(model.Book).filter_by(title=book.title).update(
            book.to_dict()
        )


class InMemoryBookRepository(AbstractBookRepository):
    books = {}

    def __init__(self):
        super().__init__()

    def _add(self, book):
        book.created_at = datetime.now()
        book.updated_at = datetime.now()
        self.books[book.title] = book

    def _delete(self, title):
        self.books.pop(title, None)

    def _get(self, title):
        return self.books.get(title)

    def _update(self, book):
        book.updated_at = datetime.now()
        self.books[book.title] = book
