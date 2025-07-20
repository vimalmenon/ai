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
            result = DbServiceManager().save(
                DbServiceModel(
                    id=generate_uuid(),
                    data=node.message or "",
                    wf_id=wf_id,
                    created_date=created_date(),
                ),
            )
            return {"data": result.id}
        elif node.service == ServiceModel.GetFromDB:
            return {"data": "Get from DB"}

    def get_by_id(self) -> list[DbServiceModel]:
        return DbServiceManager().get()

    def delete_by_id(self, id: str) -> None:
        """This will delete the db service by id"""
        DbServiceManager().delete_by_id(id)
