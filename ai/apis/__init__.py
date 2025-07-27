from ai.apis.blog import router as router_blog
from ai.apis.llm_data import router as router_llm_data
from ai.apis.rest import router as router_rest
from ai.apis.s3 import router as router_s3
from ai.apis.workflow import router as router_workflow
from ai.apis.workflow_execute import router as router_workflow_execute
from ai.apis.workflow_node import router as router_workflow_node

__all__ = [
    "router_workflow",
    "router_rest",
    "router_s3",
    "router_workflow_node",
    "router_workflow_execute",
    "router_llm_data",
    "router_blog",
]
