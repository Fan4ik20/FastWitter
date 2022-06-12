from database import models, settings


class DbInterface:
    @staticmethod
    def create_tables() -> None:
        models.BlogBase.metadata.create_all(bind=settings.blog_engine)
