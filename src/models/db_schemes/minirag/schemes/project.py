from .minirag_base import sqlalchemyBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Project(sqlalchemyBase):
    __tablename__  = "projects"

    project_id = Column(Integer,primary_key=True,autoincrement=True)
    project_uuid = Column(UUID(as_uuid=True),default=uuid.uuid4,unique=True,nullable=False)

    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)