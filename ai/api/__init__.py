from ai.api.agent import router as router_agent
from ai.api.contact import router as router_contact
from ai.api.rest import router as router_rest
from ai.api.s3 import router as router_s3
from ai.api.workflows import router as router_workflows

__all__ = [
    "router_contact",
    "router_workflows",
    "router_rest",
    "router_s3",
    "router_agent",
]
