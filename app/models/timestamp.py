from sqlalchemy import Column, TIMESTAMP, func

class TimestampMixin(object):
  created_at = Column(TIMESTAMP, server_default=func.now())
  updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
  disabled_at = Column(TIMESTAMP, nullable=True, default=None)