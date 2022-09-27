import pickle
from typing import Tuple

from fastapi import Depends
from redis import Redis

from app.esp32 import IESP32Service

from . import get_redis


class ESP32Service(IESP32Service):
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_machine(self, id: str) -> Tuple[int, int] | None:
        # We'll keep a mapping of the esp32 to its (floor, pos)

        res = self.redis.get(f"esp32:{id}")
        if res is None:
            return None

        return pickle.loads(res)

    def create_machine(self, id: str, floor: int, pos: int):
        info = pickle.dumps((floor, pos))

        self.redis.set(f"esp32:{id}", info)


def get_esp32_service(redis: Redis = Depends(get_redis)):
    """Fastapi dependency for getting a MachineService instance."""
    return ESP32Service(redis)
