from enum import IntEnum
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ByteSize,
    Field,
    field_serializer,
    field_validator,
)

import libclamav_py.utils.constant as constant

from .base import ConfigBase


class EngineField(IntEnum):
    max_scan_size = 0  # CL_ENGINE_MAX_SCANSIZE
    max_file_size = 1  # CL_ENGINE_MAX_FILESIZE
    max_recursion = 2  # CL_ENGINE_MAX_RECURSION
    max_files = 3  # CL_ENGINE_MAX_FILES
    structured_min_credit_card_count = 4  # CL_ENGINE_STRUCTURED_SSN_COUNT
    structured_min_ssn_count = 5  # CL_ENGINE_MIN_SSN_COUNT
    pua_categories = 6  # CL_ENGINE_PUA_CATEGORIES

    temporary_directory = 13  # CL_ENGINE_TMPDIR
    leave_temporary_files = 14  # CL_ENGINE_KEEPTMP
    bytecode_security = 15  # CL_ENGINE_BYTECODE_SECURITY
    bytecode_timeout = 16  # CL_ENGINE_BYTECODE_TIMEOUT

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


class PUAConfig(BaseModel):
    enabled: bool = False
    excludes: list[str] = []
    includes: list[str] = []

    def to_string(self) -> str | None:
        if self.enabled:
            if self.excludes:
                return ".".join(self.excludes) + "."
            if self.includes:
                return ".".join(self.includes) + "."


class EngineConfig(ConfigBase):
    max_scan_size: Optional[ByteSize] = Field(
        default=ByteSize(400 * constant.MB), alias="MaxScanSize"
    )

    max_file_size: Optional[ByteSize] = Field(
        default=ByteSize(100 * constant.MB), alias="MaxFileSize"
    )

    max_recursion: Optional[int] = Field(default=100, alias="MaxRecursion")

    max_files: Optional[int] = Field(default=10000, alias="MaxFiles")

    structured_min_credit_card_count: Optional[int] = Field(
        default=3, alias="StructuredMinCreditCardCount"
    )

    structured_min_ssn_count: Optional[int] = Field(
        default=3, alias="StructuredMinSSNCount"
    )

    temporary_directory: Optional[str] = Field(
        default="/tmp", alias="TemporaryDirectory"
    )

    leave_temporary_files: Optional[bool] = Field(
        default=False, alias="LeaveTemporaryFiles"
    )

    bytecode_security: Optional[Literal["TrustSigned", "Paranoid", "None"]] = Field(
        default="TrustSigned", alias="BytecodeSecurity"
    )
    bytecode_timeout: Optional[int] = Field(default=10000, alias="BytecodeTimeout")

    max_embedded_pe: Optional[ByteSize] = Field(
        default=ByteSize(40 * constant.MB), alias="MaxEmbeddedPE"
    )

    max_html_normalize: Optional[ByteSize] = Field(
        default=ByteSize(4 * constant.MB), alias="MaxHTMLNormalize"
    )

    max_html_notags: Optional[ByteSize] = Field(
        default=ByteSize(8 * constant.MB), alias="MaxHTMLNoTags"
    )

    max_script_normalize: Optional[ByteSize] = Field(
        default=ByteSize(20 * constant.MB), alias="MaxScriptNormalize"
    )

    max_zip_type_rcg: Optional[ByteSize] = Field(
        default=ByteSize(1 * constant.MB), alias="MaxZipTypeRcg"
    )

    force_to_disk: Optional[bool] = Field(default=False, alias="ForceToDisk")

    cache_size: Optional[int] = Field(default=65536, alias="CacheSize")

    disable_cache: Optional[bool] = Field(default=False, alias="DisableCache")

    max_partitions: Optional[int] = Field(default=50, alias="MaxPartitions")

    max_icons_pe: Optional[int] = Field(default=100, alias="MaxIconsPE")

    max_rech_wp3: Optional[int] = Field(default=16, alias="MaxRecHWP3")

    max_scan_time: Optional[int] = Field(default=120000, alias="MaxScanTime")

    pcre_match_limit: Optional[int] = Field(default=100000, alias="PCREMatchLimit")

    pcre_rec_match_limit: Optional[int] = Field(default=200, alias="PCRERecMatchLimit")

    pcre_max_file_size: Optional[ByteSize] = Field(
        default=ByteSize(400 * constant.MB), alias="PCREMaxFileSize"
    )

    disable_cert_check: Optional[bool] = Field(default=False, alias="DisableCertCheck")

    @field_serializer(
        "force_to_disk", "disable_cert_check", "disable_cache", "leave_temporary_files"
    )
    def serialize_bool(self, b: bool) -> int:
        return 1 if b else 0

    @field_validator(
        "force_to_disk",
        "disable_cert_check",
        "disable_cache",
        "leave_temporary_files",
        mode="before",
    )
    @classmethod
    def validate_bool(cls, value: int) -> bool:
        return value == 1

    @field_serializer("bytecode_security")
    def serialize_bytecode_security(
        self, v: Literal["TrustSigned", "Paranoid", "None"]
    ) -> int:
        if v == "TrustSigned":
            return 1
        elif v == "Paranoid":
            return 2
        elif v == "None":
            return 0

    @field_validator(
        "bytecode_security",
        mode="before",
    )
    @classmethod
    def validate_bytecode_security(cls, v: int | str) -> str:
        if isinstance(v, int):
            if v == 0:
                return "None"
            elif v == 2:
                return "Paranoid"
            else:
                return "TrustSigned"
        return v
