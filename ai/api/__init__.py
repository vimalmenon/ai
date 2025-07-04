from ai.api.rest import router as router_rest
from ai.api.s3 import router as router_s3
from ai.api.workflow import router as router_workflow
from ai.api.workflow_execute import router as router_workflow_execute
from ai.api.workflow_node import router as router_workflow_node

__all__ = [
    "router_workflow",
    "router_rest",
    "router_s3",
    "router_workflow_node",
    "router_workflow_execute",
]
