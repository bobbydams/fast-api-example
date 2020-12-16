import pytest

from apps.api.adapters import book_repository
from apps.api.domain import model


def init_db(session):
    book1 = model.Book("Some Book", "Some Author", "Some Publisher", 1000)
    book2 = model.Book(
        "A Different Book", "A Different Author", "A Different Publisher", 1000
    )
    session.add(book1)
    session.add(book2)
    session.commit()


def test_add_book(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = book_repository.SqlAlchemyBookRepository(session)
    book = model.Book("A Book", "An Author", "A Publisher", 1000)
    repo.add(book)


def test_update_book(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = book_repository.SqlAlchemyBookRepository(session)
    book = model.Book("A Book", "An Author", "A Publisher", 1000)
    repo.update(book)


def test_delete_book(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = book_repository.SqlAlchemyBookRepository(session)
    repo.delete(title="A Book")


@pytest.mark.parametrize(
    "title,author",
    [
        pytest.param("Some Book", "Some Author"),
        pytest.param("A Different Book", "A Different Author"),
    ],
)
def test_get_book(sqlite_session_factory, title, author):
    session = sqlite_session_factory()
    init_db(session)
    repo = book_repository.SqlAlchemyBookRepository(session)
    book = repo.get(title)

    assert book.title == title
    assert book.author == author
