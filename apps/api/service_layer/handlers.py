# pylint: disable=unused-argument
from typing import Callable, Dict, Type

from sqlalchemy.exc import IntegrityError

from apps.api.domain import commands
from apps.api.domain.exceptions import EntityNotAdded, EntityNotFound
from apps.api.service_layer import unit_of_work


def add_book(command: commands.AddBook, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        uow.books.add(book=command.book)
        try:
            uow.commit()
        except IntegrityError:
            raise EntityNotAdded("Book not added!")
    return True


def get_book(command: commands.GetBook, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        book = uow.books.get(title=command.title)
        if book:
            return book
        raise EntityNotFound(f"Book by title {command.title!r} not found!")


def update_book(command: commands.UpdateBook, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        book = uow.books.get(title=command.book.title)
        if book:
            command.book.created_at = book.created_at
            uow.books.update(book=command.book)
        else:
            uow.books.add(book=command.book)
        uow.commit()
    return True


def delete_book(command: commands.DeleteBook, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        uow.books.delete(title=command.title)
        uow.commit()
    return True


COMMAND_HANDLERS = {
    commands.AddBook: add_book,
    commands.GetBook: get_book,
    commands.UpdateBook: update_book,
    commands.DeleteBook: delete_book,
}  # type: Dict[Type[commands.Command], Callable]
