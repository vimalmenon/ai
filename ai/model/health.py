from ai.model.base_model import Base
from ai.model.enums import HealthStatus


class Health(Base):
    aws: HealthStatus
    llm: HealthStatus
    status: HealthStatus
