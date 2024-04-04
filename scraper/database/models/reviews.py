# -*- coding: utf-8 -*-
from sqlalchemy import Column, text, VARCHAR, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, TEXT, TIMESTAMP, SMALLINT, DATE

from .base import Base


class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        UniqueConstraint(
            'product_code', 'external_id',
            name='unique_product_code_and_external_id'
        ),
    )

    id = Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    product_code = Column(VARCHAR(64), index=True, unique=False, nullable=True)
    product_code_1 = Column(VARCHAR(64), index=True, unique=False, nullable=True)
    external_id = Column(VARCHAR(64), index=True, unique=False, nullable=True)
    review_body = Column(TEXT(), index=False, unique=False, nullable=True)
    rating_number = Column(SMALLINT(), index=False, unique=False, nullable=True,  default=0, server_default=text('0'))
    author = Column(VARCHAR(192), index=False, unique=False, nullable=True)
    post_date = Column(DATE(), index=False, unique=False, nullable=True)

    created_at = Column("created_at", TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), )
    updated_at = Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        index=True,
        unique=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )
