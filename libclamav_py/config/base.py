import ctypes

from pydantic import BaseModel, ConfigDict


class ConfigBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def _to_bit_flag(self) -> ctypes.c_uint32:
        pass
