from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select, create_engine, exists
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Ad(Base):
    __tablename__ = "ad"
    id: Mapped[str] = mapped_column(primary_key=True)
    is_business: Mapped[bool]
    title: Mapped[str]
    description: Mapped[str]
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
        Base.metadata.create_all(self.__engine)

    def exists(self, data=None, id=None) -> bool:
        """
        Checks if a specific ad exists either from JSON ad data, or a specified ad ID.
        :param data: JSON ad data.
        :param id: Ad ID.
        :return: Returns true if the ad already exists in the database.
        """
        session = Session(self.__engine)
        id = id if id is not None else data.get('@id')
        return session.query(exists(Ad).where(Ad.id == id)).scalar()

    def save_ad(self, data) -> Ad:
        """
        Parses an ad from JSON ad data, and saves it to the database.
        :param data: The JSON ad data.
        :return: Returns the ad as an object.
        """
        id = data.get('@id')
        is_business = id[0] == 'm'
        title = data.get('ad:title')
        description = data.get('ad:description')
        type = data.get('ad:ad-type').get('ad:value').capitalize()
        price = "Wanted" if type == "Wanted" \
            else "Please Contact" if data.get('ad:price').get('types:amount') is None \
            else data.get('ad:price').get('types:amount')
        user_id = data.get('ad:user-id')
        datetime_scraped = datetime.now(timezone.utc)
        datetime_creation = datetime.strptime(data.get('ad:creation-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
        datetime_start = datetime.strptime(data.get('ad:start-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc)
        datetime_end = datetime.strptime(data.get('ad:end-date-time'), '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc) if data.get('ad:end-date-time') is not None else None
        image = data.get('pic:pictures').get('pic:picture') if data.get('pic:pictures') is not None else None
        if isinstance(image, list):
            image = image[0].get('pic:link')
        elif isinstance(image, dict):
            image = image.get('pic:link')
        if image is not None:
            for i in range(len(image)):
                if image[i].get('@rel') == 'extraLarge':
                    image = image[i].get('@href')

        session = Session(self.__engine)
        ad = Ad(id=id,
                is_business=is_business,
                title=title,
                description=description,
                type=type,
                price=price,
                user_id=user_id,
                datetime_scraped=datetime_scraped,
                datetime_creation=datetime_creation,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                image=image
                )
        session.add(ad)
        session.commit()
        return ad

    def close(self):
        self.__engine.dispose()
