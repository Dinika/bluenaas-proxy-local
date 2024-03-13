from enum import StrEnum


# TODO: NOTE: do we keep the suffix ERROR or not ?
class NexusErrorValue(StrEnum):
    CREATE_PROJECT_ERROR = "NEXUS_CREATE_PROJECT_ERROR"
    DEPRECATE_PROJECT_ERROR = "NEXUS_DEPRECATE_PROJECT_ERROR"
    CREATE_PROJECT_ACL_ERROR = "NEXUS_CREATE_PROJECT_ACL_ERROR"
    CREATE_RESOURCE_ERROR = "NEXUS_CREATE_RESOURCE_ERROR"
    CREATE_RESOLVER_ERROR = "NEXUS_CREATE_RESOLVER_ERROR"
    CREATE_ES_VIEW_ERROR = "NEXUS_CREATE_ES_VIEW_ERROR"
    CREATE_SP_VIEW_ERROR = "NEXUS_CREATE_SP_VIEW_ERROR"
    CREATE_ES_AGG_VIEW_ERROR = "NEXUS_CREATE_ES_AGG_VIEW_ERROR"
    CREATE_SP_AGG_VIEW_ERROR = "NEXUS_CREATE_SP_AGG_VIEW_ERROR"
    FETCH_RESOURCE_ERROR = "NEXUS_FETCH_RESOURCE_ERROR"
    GENERIC_ERROR = "NEXUS_GENERIC_ERROR"


class NexusError(Exception):
    message: str | None
    type: NexusErrorValue | None

    def __init__(
        self, *, message: str | None = None, type: NexusErrorValue | None = None
    ) -> None:
        self.message = message
        self.type = type
        super().__init__(self.message)
