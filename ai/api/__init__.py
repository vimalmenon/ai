from ai.api.contact import router as router_contact
from ai.api.rest import router as router_rest
from ai.api.s3 import router as router_s3
from ai.api.workflow import router as router_workflow

__all__ = ["router_contact", "router_workflow", "router_rest", "router_s3"]
