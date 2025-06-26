from ai.model.base_model import Base


class ResumeWorkflowRequest(Base):
    id: str
    value: str | None = None
