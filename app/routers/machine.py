from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from app.auth import validate_api_key
from app.esp32 import IESP32Service
from app.machine import (
    IMachineService,
    Machine,
    MachineFilter,
    MachineStatus,
    MachineType,
    MachineUpdate,
    _field_floor,
    _field_pos,
    _field_status,
    _field_type,
)
from app.redis.esp32 import get_esp32_service
from app.redis.machine import get_machine_service

router = APIRouter(prefix="/machine")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    description="Creates a new machine.",
    dependencies=[Depends(validate_api_key)],
)
async def create_machine(
    m: Machine, ms: IMachineService = Depends(get_machine_service)
) -> None:
    ms.create(m.to_machine_x())


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[Machine],
    description="Get a list of machines.",
)
async def get_machines(
    status: Optional[MachineStatus] = Query(
        None, description=_field_status.description
    ),
    floor: Optional[int] = Query(None, description=_field_floor.description),
    pos: Optional[int] = Query(None, description=_field_pos.description),
    type: Optional[MachineType] = Query(None, description=_field_type.description),
    ms: IMachineService = Depends(get_machine_service),
) -> List[Machine]:
    mf = MachineFilter(status=status, floor=floor, pos=pos, type=type)
    return [m.to_machine() for m in ms.find(mf)]


@router.put(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Machine,
    description="Perform partial update of a machine. Use the /start and /stop endpoints instead if setting machine state.",
    dependencies=[Depends(validate_api_key)],
)
async def update_machine(
    mu: MachineUpdate,
    floor: int = Query(..., description=_field_floor.description),
    pos: int = Query(..., description=_field_pos.description),
    ms: IMachineService = Depends(get_machine_service),
) -> Machine:
    return ms.update(floor, pos, mu.to_machine_update_x()).to_machine()


@router.put(
    "/v2",
    status_code=status.HTTP_200_OK,
    response_model=Machine,
    description="Perform partial update of a machine. Use the /start and /stop endpoints instead if setting machine state.",
    dependencies=[Depends(validate_api_key)],
)
async def update_machine_esp(
    mu: MachineUpdate,
    x_esp_id: str = Header(default=None),
    ms: IMachineService = Depends(get_machine_service),
    es: IESP32Service = Depends(get_esp32_service),
) -> Machine:
    if x_esp_id is None:
        raise HTTPException(status_code=400, detail="No X-Esp-32 header")

    m = es.get_machine(x_esp_id)
    if m is None:
        raise HTTPException(status_code=400, detail="No ESP32 found with that ID")

    return ms.update(m[0], m[1], mu.to_machine_update_x()).to_machine()


@router.put(
    "/start",
    status_code=status.HTTP_202_ACCEPTED,
    description="Start this machine.",
    dependencies=[Depends(validate_api_key)],
)
async def start_machine(
    floor: int = Query(..., description=_field_floor.description),
    pos: int = Query(..., description=_field_pos.description),
    ms: IMachineService = Depends(get_machine_service),
):
    return ms.start(floor, pos)


@router.put(
    "/v2/start",
    status_code=status.HTTP_202_ACCEPTED,
    description="Start this machine.",
    dependencies=[Depends(validate_api_key)],
)
async def start_machine_esp(
    x_esp_id: str = Header(default=None),
    es: IESP32Service = Depends(get_esp32_service),
    ms: IMachineService = Depends(get_machine_service),
):
    if x_esp_id is None:
        raise HTTPException(status_code=400, detail="No X-Esp-32 header")

    m = es.get_machine(x_esp_id)
    if m is None:
        raise HTTPException(status_code=400, detail="No ESP32 found with that ID")

    return ms.start(m[0], m[1])


@router.put(
    "/stop",
    status_code=status.HTTP_202_ACCEPTED,
    description="Stop this machine.",
    dependencies=[Depends(validate_api_key)],
)
async def stop_machine(
    floor: int = Query(..., description=_field_floor.description),
    pos: int = Query(..., description=_field_pos.description),
    ms: IMachineService = Depends(get_machine_service),
):
    return ms.stop(floor, pos)


@router.put(
    "/v2/stop",
    status_code=status.HTTP_202_ACCEPTED,
    description="Stop this machine.",
    dependencies=[Depends(validate_api_key)],
)
async def stop_machine_esp(
    x_esp_id: str = Header(default=None),
    es: IESP32Service = Depends(get_esp32_service),
    ms: IMachineService = Depends(get_machine_service),
):
    if x_esp_id is None:
        raise HTTPException(status_code=400, detail="No X-Esp-32 header")

    m = es.get_machine(x_esp_id)
    if m is None:
        raise HTTPException(status_code=400, detail="No ESP32 found with that ID")

    return ms.stop(m[0], m[1])


esprouter = APIRouter(prefix="/esp")


@esprouter.post(
    "/esp",
    status_code=status.HTTP_200_OK,
    description="Map an ESP32's ID to some machine.",
    dependencies=[Depends(validate_api_key)],
)
async def create_esp(
    id: str = Query(..., description="The ESP32's unique ID."),
    floor: int = Query(..., description=_field_floor.description),
    pos: int = Query(..., description=_field_pos.description),
    es: IESP32Service = Depends(get_esp32_service),
):
    es.create_machine(id, floor, pos)
