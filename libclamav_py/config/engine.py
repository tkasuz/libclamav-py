from typing import Optional

from pydantic import Field, field_serializer

import libclamav_py.utils.constant as constant

from .base import ConfigBase


class EngineConfig(ConfigBase):
    max_scan_size: Optional[int] = Field(
        default=400 * constant.MB, alias="CL_ENGINE_MAX_SCANSIZE"
    )

    max_file_size: Optional[int] = Field(
        default=100 * constant.MB, alias="CL_ENGINE_MAX_FILESIZE"
    )

    max_recursion: Optional[int] = Field(default=100, alias="CL_ENGINE_MAX_RECURSION")

    max_files: Optional[int] = Field(default=10000, alias="CL_ENGINE_MAX_FILES")

    structured_min_credit_card_count: Optional[int] = Field(
        default=3, alias="CL_ENGINE_MIN_CC_COUNT"
    )

    structured_min_ssn_count: Optional[int] = Field(
        default=3, alias="CL_ENGINE_MIN_SSN_COUNT"
    )

    max_embedded_pe: Optional[int] = Field(
        default=40 * constant.MB, alias="CL_ENGINE_MAX_EMBEDDEDPE"
    )

    max_html_normalize: Optional[int] = Field(
        default=4 * constant.MB, alias="CL_ENGINE_MAX_HTMLNORMALIZE"
    )

    max_html_notags: Optional[int] = Field(
        default=8 * constant.MB, alias="CL_ENGINE_MAX_HTMLNOTAGS"
    )

    max_script_normalize: Optional[int] = Field(
        default=20 * constant.MB, alias="CL_ENGINE_MAX_SCRIPTNORMALIZE"
    )

    max_zip_type_rcg: Optional[int] = Field(
        default=1 * constant.MB, alias="CL_ENGINE_MAX_SCRIPTNORMALIZE"
    )

    force_to_disk: Optional[bool] = Field(default=False, alias="CL_ENGINE_FORCETODISK")

    cache_size: Optional[int] = Field(default=65536, alias="CL_ENGINE_CACHE_SIZE")

    disable_cache: Optional[bool] = Field(
        default=False, alias="CL_ENGINE_DISABLE_CACHE"
    )

    max_partitions: Optional[int] = Field(default=50, alias="CL_ENGINE_MAX_PARTITIONS")

    max_icons_pe: Optional[int] = Field(default=100, alias="CL_ENGINE_MAX_ICONSPE")

    max_rech_wp3: Optional[int] = Field(default=16, alias="CL_ENGINE_MAX_RECHWP3")

    max_scan_time: Optional[int] = Field(default=120000, alias="CL_ENGINE_MAX_SCANTIME")

    pcre_match_limit: Optional[int] = Field(
        default=100000, alias="CL_ENGINE_PCRE_MATCH_LIMIT"
    )

    pcre_rec_match_limit: Optional[int] = Field(
        default=200, alias="CL_ENGINE_PCRE_RECMATCH_LIMIT"
    )

    pcre_max_file_size: Optional[int] = Field(
        default=400 * constant.MB, alias="CL_ENGINE_PCRE_MAX_FILESIZE"
    )

    disable_cert_check: Optional[bool] = Field(
        default=False, alias="CL_ENGINE_DISABLE_PE_CERTS"
    )

    @field_serializer("force_to_disk", "disable_cert_check", "disable_cache")
    def serialize_bool(self, b: bool) -> int:
        return 1 if b else 0
