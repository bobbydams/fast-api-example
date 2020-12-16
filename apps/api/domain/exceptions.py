from apps.api.domain.library import DomainException


class BookNotAdded(DomainException):
    code = "BOOK_NOT_ADDED"
    status_code = 500


class BookNotFound(DomainException):
    code = "BOOK_NOT_FOUND"
    status_code = 404