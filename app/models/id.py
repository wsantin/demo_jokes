from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, text, Integer

type_id_hex = String(12)
type_id_int = Integer
type_id_uuid = UUID(as_uuid=True)

class IdInt:
  id = Column(type_id_int,
                 primary_key=True,
                 unique=True,
                 nullable=False)
  
class IdHex:
  id = Column(type_id_hex,
                 primary_key=True,
                 server_default=text("to_hex(FLOOR(EXTRACT(epoch FROM NOW())*10000)::bigint)"),
                 unique=True,
                 nullable=False)

class IdUuid:
  id = Column(type_id_uuid,
                 primary_key=True,
                 server_default=text('UUID()'),
                 unique=True,
                 nullable=False)