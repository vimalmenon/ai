from ai.api.contact import router as router_contact
from ai.api.llm import router as router_llm
from ai.api.rest import router as router_rest
from ai.api.workflow import router as router_workflow

__all__ = ["router_contact", "router_workflow", "router_llm", "router_rest"]
