"""SQLAlchemy base & model registry"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """base class for all SQLAlchemy models"""