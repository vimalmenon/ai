from ai.model.health import Health, HealthStatus


class HealthService:
    def get_status(self) -> Health:
        return Health(llm=HealthStatus.OK, status=HealthStatus.OK, aws=HealthStatus.OK)
