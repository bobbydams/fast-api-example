from dataclasses import dataclass

from apps.api.domain import model


class Command:
    pass


@dataclass
class AddBook(Command):
    book: model.Book


@dataclass
class GetBook(Command):
    title: str


@dataclass
class UpdateBook(Command):
    book: model.Book


@dataclass
class DeleteBook(Command):
    title: str