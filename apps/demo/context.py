from apps.demo.adapter import remote_book_service


class Context:
    def __init__(self):
        self.book_service = remote_book_service.RemoteBookService(
            "http://localhost:5000"
        )
