from enum import IntEnum
from typing import Optional

from pydantic import Field, field_serializer, field_validator

import libclamav_py.utils.constant as constant

from .base import ConfigBase


class EngineField(IntEnum):
    max_scan_size = 0  # CL_ENGINE_MAX_SCANSIZE
    max_file_size = 1  # CL_ENGINE_MAX_FILESIZE
    max_recursion = 2  # CL_ENGINE_MAX_RECURSION
    max_files = 3  # CL_ENGINE_MAX_FILES
    structured_min_credit_card_count = 4  # CL_ENGINE_STRUCTURED_SSN_COUNT
    structured_min_ssn_count = 5  # CL_ENGINE_MIN_SSN_COUNT
    max_embedded_pe = 18  # CL_ENGINE_MAX_EMBEDDEDPE
    max_html_normalize = 19  # CL_ENGINE_MAX_HTMLNORMALIZE
    max_html_notags = 20  # CL_ENGINE_MAX_HTMLNOTAGS
    max_script_normalize = 21  # CL_ENGINE_MAX_SCRIPTNORMALIZE
    max_zip_type_rcg = 22  # CL_ENGINE_MAX_ZIPTYPERCG
    force_to_disk = 23  # CL_ENGINE_FORCE_TO_DISK
    cache_size = 24  # CL_ENGINE_CACHE_SIZE
    disable_cache = 25  # CL_ENGINE_DISABLE_CACHE
    max_partitions = 28  # CL_ENGINE_MAX_PARTITIONS
    max_icons_pe = 29  # CL_ENGINE_MAX_ICONSPE
    max_rech_wp3 = 30  # CL_ENGINE_MAX_RECHWP3
    max_scan_time = 31  # CL_ENGINE_MAX_SCANTIME
    pcre_match_limit = 32  # CL_ENGINE_PCRE_MATCHLIMIT
    pcre_rec_match_limit = 33  # CL_ENGINE_PCRE_RECMATCHLIMIT
    pcre_max_file_size = 34  # CL_ENGINE_PCRE_MAXFILESIZE
    disable_cert_check = 35  # CL_ENGINE_DISABLE_CERT_CHECK


class EngineConfig(ConfigBase):
    max_scan_size: Optional[int] = Field(
        default=400 * constant.MB,
    )

    max_file_size: Optional[int] = Field(
        default=100 * constant.MB,
    )

    max_recursion: Optional[int] = Field(default=100)

    max_files: Optional[int] = Field(default=10000)

    structured_min_credit_card_count: Optional[int] = Field(default=3)

    structured_min_ssn_count: Optional[int] = Field(default=3)

    max_embedded_pe: Optional[int] = Field(default=40 * constant.MB)

    max_html_normalize: Optional[int] = Field(default=4 * constant.MB)

    max_html_notags: Optional[int] = Field(default=8 * constant.MB)

    max_script_normalize: Optional[int] = Field(default=20 * constant.MB)

    max_zip_type_rcg: Optional[int] = Field(default=1 * constant.MB)

    force_to_disk: Optional[bool] = Field(default=False)

    cache_size: Optional[int] = Field(default=65536)

    disable_cache: Optional[bool] = Field(default=False)

    max_partitions: Optional[int] = Field(default=50)

    max_icons_pe: Optional[int] = Field(default=100)

    max_rech_wp3: Optional[int] = Field(default=16)

    max_scan_time: Optional[int] = Field(default=120000)

    pcre_match_limit: Optional[int] = Field(default=100000)

    pcre_rec_match_limit: Optional[int] = Field(default=200)

    pcre_max_file_size: Optional[int] = Field(default=400 * constant.MB)

    disable_cert_check: Optional[bool] = Field(default=False)

    @field_serializer("force_to_disk", "disable_cert_check", "disable_cache")
    def serialize_bool(self, b: bool) -> int:
        return 1 if b else 0

    @field_validator(
        "force_to_disk", "disable_cert_check", "disable_cache", mode="before"
    )
    @classmethod
    def validate_bool(cls, value: int) -> bool:
        return value == 1
