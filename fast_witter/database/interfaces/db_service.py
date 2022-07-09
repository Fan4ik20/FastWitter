from database import models


class DbInterface:
    @staticmethod
    def create_tables(engine) -> None:
        models.BlogBase.metadata.create_all(bind=engine)
