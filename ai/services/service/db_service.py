from ai.managers import DbServiceManager
from ai.model import (
    DbServiceModel,
    WorkflowNodeRequest,
)
from ai.model.others import Service as ServiceModel
from ai.utilities import created_date, generate_uuid


class DbService:

    def execute(self, wf_id: str, node: WorkflowNodeRequest):
        if node.service == ServiceModel.SaveToDB:
            DbServiceManager().save(
                DbServiceModel(
                    id=generate_uuid(),
                    data=node.message or "",
                    wf_id=wf_id,
                    created_date=created_date(),
                ),
            )
            return {"data": "Saved to DB"}
        elif node.service == ServiceModel.GetFromDB:
            return {"data": "Get from DB"}

    def get_by_id(self) -> list[DbServiceModel]:
        return DbServiceManager().get()
