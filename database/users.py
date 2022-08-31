from __future__ import annotations
from .db import Base
import random
import string

from sqlalchemy import Column, DateTime, text, exists
from sqlalchemy.dialects.mysql import BIGINT, ENUM, VARCHAR
from utils import nickname as nickname_util

class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True)
    social_id = Column(VARCHAR(256), unique=True)
    nickname = Column(VARCHAR(50), unique=True)
    social_type = Column(ENUM('kakao', 'google'))
    email = Column(VARCHAR(320))
    secret = Column(VARCHAR(36), server_default=text("UUID()"))
    picture = Column(VARCHAR(32))
    status = Column(ENUM('active', 'inactive', 'banned', 'deleted'), server_default='active')
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP()"))

    @staticmethod
    def exists_nickname(sess, nickname) -> bool:
        return sess.query(exists().where(User.nickname == nickname)).scalar()

    @staticmethod
    def create_nickname(sess) -> str: # idk session type :(
        while True:
            nickname = f'{nickname_util.choice()}_{"".join(random.choices(string.digits, k=8))}'

            if not User.exists_nickname(sess, nickname):
                return nickname

    @staticmethod
    def session_get(sess, id: int) -> User | None:
        return sess.query(User).filter(User.id == id).first()