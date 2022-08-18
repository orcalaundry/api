import re
from datetime import datetime

from pydantic import BaseModel, validator

from app.machine import MachineType


class UsageDetail(BaseModel):
    """
    UsageDetail represents one instance of some machine being used.
    """

    loc: str
    type: MachineType
    started_at: datetime
    stopped_at: datetime

    @validator("loc")
    def loc_is_correct_format(cls, v):
        """ "
        So basically the `loc` field should have a format like "washer:5:0"
        meaning it's a washer on the 5th floor, position 0.
        """
        if re.match(r"^(washer|dryer):\d+:\d+$", v) is None:
            raise ValueError("loc format is invalid")
        return v
