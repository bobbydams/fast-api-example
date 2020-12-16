from fastapi import APIRouter

from apps.api.context import Context
from apps.api.domain import commands, model

context = Context()
router = APIRouter()


@router.post("/book")
async def add(book: model.Book):
    command = commands.AddBook(book=book)
    context.messagebus.handle(command)
    return dict(success=True)


@router.get("/book/{title}")
async def get(title):
    command = commands.GetBook(title=title)
    book = context.messagebus.handle(command)
    return book


@router.put("/book")
async def update(book: model.Book):
    command = commands.UpdateBook(book=book)
    result = context.messagebus.handle(command)
    return dict(success=result)


@router.delete("/book/{title}")
async def delete(title):
    command = commands.DeleteBook(title=title)
    result = context.messagebus.handle(command)
    return dict(success=result)