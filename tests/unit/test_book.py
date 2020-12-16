from apps.api.domain import model


def test_book():
    book = model.Book(
        title="A Book", author="An Author", publisher="A Publisher", pages=1000
    )

    assert book.title == "A Book"
    assert book.author == "An Author"
    assert book.publisher == "A Publisher"
    assert book.pages == 1000