import logging
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import mapper, relationship

from apps.api.domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()

books = Table(
    'books',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), unique=True),
    Column('author', String(255)),
    Column('publisher', String(255)),
    Column('pages', Integer, nullable=False),
    Column('tag_id', ForeignKey('tags.id')),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

tags = Table(
    'tags',
    metadata,
    Column('id', String(255), primary_key=True),
    Column('name', String(255)),
)


def start_mappers():
    logger.info("Starting mappers")
    tags_mapper = mapper(model.Tag, tags)
    mapper(
        model.Book,
        books,
        properties={
            '_tags': relationship(
                tags_mapper,
                collection_class=set,
            )
        },
    )
