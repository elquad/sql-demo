from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    Text,
    Index,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import INET


Base = declarative_base()


class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)


class Url(Base):
    __tablename__ = "url"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    url = Column(Text, unique=True, nullable=False)
    source_id = Column(Integer, nullable=False)

    __table_args__ = (
        # Substring / fuzzy search accelerator
        Index(
            "ix_url_trgm",
            "url",
            postgresql_using="gin",
            postgresql_ops={"url": "gin_trgm_ops"},
        ),
    )


class Ip(Base):
    __tablename__ = "ip"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    address = Column(INET, nullable=False, unique=True)
    source_id = Column(Integer, nullable=False)