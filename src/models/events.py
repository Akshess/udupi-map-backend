from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    cost: Mapped[float]
    description: Mapped[str]
    organizer: Mapped[str]
    phone_number: Mapped[int]
    date: Mapped[str]
    email: Mapped[str]
    location: Mapped[str]