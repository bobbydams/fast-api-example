import abc
from datetime import datetime

from apps.api.domain import model
from apps.api.domain.exceptions import EntityNotFound


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


class MongoBookRepository(AbstractBookRepository):
    def __init__(self, mongo_config):
        super().__init__()
        self.client = mongo_config.client
        self.db = self.client[mongo_config.db]
        self.collection = "books"

    def _add(self, entity):
        self.db[self.collection].insert(entity.to_dict())

    def _filter(self, filter, limit: int, skip: int):
        docs = list(self.db[self.collection].find(filter, limit=limit, skip=skip))
        return [model.Book(**doc) for doc in docs]

    def _delete(self, id):
        self.db[self.collection].delete_one(dict(_id=id))

    def _get(self, id):
        doc = self.db[self.collection].find_one(dict(_id=id))
        if not doc:
            raise EntityNotFound(
                f"({self.__class__.__name__}) Entity with id {id!r} not found!"
            )
        return model.Book(**doc)

    def _update(self, entity):
        self.db[self.collection].update_one(
            dict(_id=entity.id), {"$set": entity.to_dict()}
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
