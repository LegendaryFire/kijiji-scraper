from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, create_engine, exists, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from constants import Changes


class Base(DeclarativeBase):
    pass


class Ad(Base):
    __tablename__ = "ad"
    id: Mapped[str] = mapped_column(primary_key=True)
    is_business: Mapped[bool]
    title: Mapped[str]
    description: Mapped[Optional[str]]
    type: Mapped[str]
    price: Mapped[str]
    user_id: Mapped[str]
    datetime_scraped: Mapped[datetime]
    datetime_creation: Mapped[datetime]
    datetime_start: Mapped[datetime]
    datetime_end: Mapped[Optional[datetime]]
    image: Mapped[Optional[str]]


class Database:
    def __init__(self, filename="default.db"):
        self.__engine = create_engine('sqlite:///default.db')
        self.__engine.connect()
        self.__session = Session(self.__engine)
        Base.metadata.create_all(self.__engine)

    def exists(self, data: Ad or dict or str) -> bool:
        """
        Checks if a specific ad exists either from JSON ad data, an Ad object or an ad ID.
        :param data: The ad ID as a string, JSON ad data or an Ad object.
        :return: Returns true if the ad already exists in the database.
        """
        if isinstance(data, str):
            return self.__session.query(exists(Ad).where(Ad.id == data)).scalar()
        elif isinstance(data, Ad):
            return self.__session.query(exists(Ad).where(Ad.id == data.id)).scalar()
        elif isinstance(data, dict):
            return self.__session.query(exists(Ad).where(Ad.id == data.get("@id"))).scalar()
        else:
            raise TypeError(f"Expected an Ad or string, not {type(data)}.")

    def compare(self, ad: Ad, replace=False) -> [Changes]:
        """
        Compares the given ad with the one stored in the database.
        :param ad: The ad to compare to.
        :param replace: Overwrite the stored ad with the given ad. Default False.
        :return: Returns a list of Changes enumerators.
        """
        stored_ad = self.__session.query(Ad).get(ad.id)
        changes = []
        if stored_ad.price != ad.price:
            changes.append(Changes.PRICE)
        if (len(changes) > 0) and replace:
            self.__session.execute(delete(Ad).where(Ad.id == ad.id))
            self.__session.add(ad)
            self.__session.commit()
        return changes

    def save_ad(self, ad: Ad) -> bool:
        """
        Takes an Ad object and saves it to the database.
        :param ad: The ad to be saved.
        :return: Returns True if saves successfully. False otherwise.
        """
        self.__session.add(ad)
        self.__session.commit()
        return True

    def close(self):
        self.__session.close()
        self.__engine.dispose()
