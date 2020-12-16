import inspect
import logging
import os

from dotenv import load_dotenv

from apps.api.adapters import orm
from apps.api import config
from apps.api.service_layer import handlers, messagebus, unit_of_work

load_dotenv("var/.env")


class ContextException(Exception):
    pass


class Context:
    instance = None

    def __init__(self):
        if not Context.instance:
            self.load()
            Context.instance = self

    def __getattr__(self, item):
        if item not in dir(self.instance):
            raise ContextException(f"Context doesn't provide {item!r}.")
        return getattr(self.instance, item)

    def all(self):
        yield self.book_repository

    def load(self):
        self.logger = logging.getLogger(__name__)

        self.load_uow("inmemory")

        dependencies = {'uow': self.uow}

        injected_command_handlers = {
            command_type: self._inject_dependencies(handler, dependencies)
            for command_type, handler in handlers.COMMAND_HANDLERS.items()
        }

        self.messagebus = messagebus.MessageBus(
            uow=self.uow,
            command_handlers=injected_command_handlers,
        )

    def load_uow(self, default):
        self.uow = self._load_uow(os.getenv('BOOK_REPOSITORY_BACKEND', default))

    def _load_uow(self, backend):
        self.logger.info(f"Loading {backend!r} UnitOfWork")
        if backend == "sqlite":
            from sqlalchemy import create_engine

            from apps.api.service_layer.unit_of_work import SqlAlchemyUnitOfWork

            orm.start_mappers()
            engine = create_engine(
                config.get_database_uri(), connect_args={"check_same_thread": False}
            )
            orm.metadata.create_all(engine)
            return SqlAlchemyUnitOfWork()
        from apps.api.service_layer.unit_of_work import InMemoryUnitOfWork

        return InMemoryUnitOfWork()

    def _inject_dependencies(self, handler, dependencies):
        params = inspect.signature(handler).parameters
        deps = {
            name: dependency
            for name, dependency in dependencies.items()
            if name in params
        }
        return lambda message: handler(message, **deps)
