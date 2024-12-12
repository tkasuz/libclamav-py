import ctypes
from typing import Optional

from pydantic import Field

from .base import ConfigBase


class DatabaseConfig(ConfigBase):
    phishing_signatures: Optional[bool] = Field(default=True)
    phishing_scan_urls: Optional[bool] = Field(default=True)
    detect_pua: Optional[bool] = Field(default=False)
    official_database_only: Optional[bool] = Field(default=False)
    bytecode: Optional[bool] = Field(default=True)

    def _to_bit_flag(self) -> ctypes.c_uint32:
        return ctypes.c_uint32(
            (0x2 if self.phishing_signatures else 0)
            | (0x8 if self.phishing_scan_urls else 0)
            | (0x10 if self.detect_pua else 0)
            | (0x1000 if self.official_database_only else 0)
            | (0x2000 if self.bytecode else 0)
        )
