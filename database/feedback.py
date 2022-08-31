from __future__ import annotations
from .db import Base

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, BIGINT, DATETIME

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(BIGINT, primary_key=True)
    user_id = Column(BIGINT, nullable=False)
    feedback = Column(VARCHAR(1000))
    info = Column(VARCHAR(6000))
    updated_at = Column(DATETIME, nullable=False, server_default='CURRENT_TIMESTAMP')

    @staticmethod
    def session_write(sess, user_id: int, feedback: str, info: str):
        feedback = Feedback(user_id=user_id, feedback=feedback, info=info)
        sess.add(feedback)
        sess.commit()
