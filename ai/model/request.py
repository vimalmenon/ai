from ai.model.base_model import Base


class ResumeWorkflowRequest(Base):
    id: str
    data: str | None = None
