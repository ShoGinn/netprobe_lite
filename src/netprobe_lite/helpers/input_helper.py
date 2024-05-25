# Input validation functions

from uuid import UUID


def is_uuid_4(uuid: str, version: int = 4) -> bool:
    try:
        UUID(uuid, version=version)
    except ValueError:
        return False
    return True
