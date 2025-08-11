from ai.managers import SchedulerProcessManager


class SchedulerProcessService:

    def process_data(self):
        items = SchedulerProcessManager().get_all_unprocessed_data()
        for _item in items:
            pass
