from ai.model import SchedulerProcessModel
from ai.model.enums import DbTable


class SchedulerProcessManager:
    table = DbTable.AI_SCHEDULER.value

    def get_all_unprocessed_data(self) -> list[SchedulerProcessModel]:
        return []
