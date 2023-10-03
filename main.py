from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


from config import SQLALCHEMY_URL
from config import SQLALCHEMY_ECHO

from tabel import Base


engine = create_engine(
    url=SQLALCHEMY_URL,
    echo=SQLALCHEMY_ECHO,
)


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("Start")
    main()
