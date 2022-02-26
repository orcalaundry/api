from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder

from app.config import get_settings
from app.machine import IMachineService, MachineFilter
from app.usage import UsageDetail


async def create(floor: int, pos: int, db: Any, ms: IMachineService) -> None:
    """
    Creates an entry for one usage instance in dynamodb.
    """
    table = db.Table(get_settings().dynamodb_usage_table)
    res = ms.find(MachineFilter(floor=floor, pos=pos))[0]
    ud = UsageDetail(
        loc=res.create_key(),
        type=res.type,
        started_at=res.last_started_at,
        stopped_at=datetime.utcnow(),
    )
    table.put_item(Item=jsonable_encoder(ud))
