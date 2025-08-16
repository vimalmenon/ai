from collections.abc import Callable

from ai.model.enums import Tool
from ai.services.tool_service.internet_search.internet_search import internet_search
from ai.services.tool_service.save_to_db.save_to_db import save_to_db
from ai.services.tool_service.save_to_s3.save_to_s3 import save_to_s3


class ToolService:

    def get_tool_func(self, name: Tool) -> Callable:
        if name == Tool.SaveToDB:
            return save_to_db
        if name == Tool.SaveToS3:
            return save_to_s3
        if name == Tool.InternetSearch:
            return internet_search
