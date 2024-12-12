import ctypes
from typing import Optional

from pydantic import BaseModel, Field

from .base import ConfigBase


class GeneralConfig(ConfigBase):
    all_match_scan: Optional[bool] = Field(default=True)
    heuristic_alerts: Optional[bool] = Field(default=True)
    heuristic_scan_precedence: Optional[bool] = Field(default=False)
    generate_metadata_json: Optional[bool] = Field(default=False)
    json_store_html_urls: Optional[bool] = Field(default=True)

    def _to_bit_flag(self) -> ctypes.c_uint32:
        return ctypes.c_uint32(
            (0x1 if self.all_match_scan else 0)
            | (0x2 if self.generate_metadata_json else 0)
            | (0x4 if self.heuristic_alerts else 0)
            | (0x8 if self.heuristic_scan_precedence else 0)
            | (0x20 if self.json_store_html_urls else 0)
        )


class ParseConfig(ConfigBase):
    scan_archive: Optional[bool] = Field(default=True)
    scan_elf: Optional[bool] = Field(default=True)
    scan_pdf: Optional[bool] = Field(default=True)
    scan_swf: Optional[bool] = Field(default=True)
    scan_hwp3: Optional[bool] = Field(default=True)
    scan_xmldocs: Optional[bool] = Field(default=True)
    scan_mail: Optional[bool] = Field(default=True)
    scan_ole2: Optional[bool] = Field(default=True)
    scan_html: Optional[bool] = Field(default=True)
    scan_pe: Optional[bool] = Field(default=True)
    scan_one_note: Optional[bool] = Field(default=True)
    scan_image: Optional[bool] = Field(default=True)
    scan_image_fuzzy_hash: Optional[bool] = Field(default=True)

    def _to_bit_flag(self) -> ctypes.c_uint32:
        return ctypes.c_uint32(
            (0x1 if self.scan_archive else 0)
            | (0x2 if self.scan_elf else 0)
            | (0x4 if self.scan_pdf else 0)
            | (0x8 if self.scan_swf else 0)
            | (0x10 if self.scan_hwp3 else 0)
            | (0x20 if self.scan_xmldocs else 0)
            | (0x40 if self.scan_mail else 0)
            | (0x80 if self.scan_ole2 else 0)
            | (0x100 if self.scan_html else 0)
            | (0x200 if self.scan_pe else 0)
            | (0x400 if self.scan_one_note else 0)
            | (0x800 if self.scan_image else 0)
            | (0x1000 if self.scan_image_fuzzy_hash else 0)
        )


class HeuristicConfig(ConfigBase):
    alert_broken: Optional[bool] = Field(default=False)

    alert_exceeds_max: Optional[bool] = Field(default=False)

    alert_phishing_ssl: Optional[bool] = Field(default=False)

    alert_phishing_cloak: Optional[bool] = Field(default=False)

    alert_macros: Optional[bool] = Field(default=False)

    alert_encrypted: Optional[bool] = Field(default=False)

    alert_encrypted_archive: Optional[bool] = Field(default=False)

    alert_encrypted_doc: Optional[bool] = Field(default=False)

    alert_partition_intersection: Optional[bool] = Field(default=False)

    structured_data_detection: Optional[bool] = Field(default=False)

    structured_ssn_format_normal: Optional[bool] = Field(default=False)

    structured_ssn_format_stripped: Optional[bool] = Field(default=False)

    structured_cc_only: Optional[bool] = Field(default=False)

    alert_broken_media: Optional[bool] = Field(default=False)

    def _to_bit_flag(self) -> ctypes.c_uint32:
        if self.alert_encrypted:
            self.alert_encrypted_archive = True
            self.alert_encrypted_doc = True
        return ctypes.c_uint32(
            (0x2 if self.alert_broken else 0)
            | (0x4 if self.alert_exceeds_max else 0)
            | (0x8 if self.alert_phishing_ssl else 0)
            | (0x10 if self.alert_phishing_cloak else 0)
            | (0x20 if self.alert_macros else 0)
            | (0x40 if self.alert_encrypted_archive else 0)
            | (0x80 if self.alert_encrypted_doc else 0)
            | (0x100 if self.alert_partition_intersection else 0)
            | (0x200 if self.structured_data_detection else 0)
            | (0x400 if self.structured_ssn_format_normal else 0)
            | (0x800 if self.structured_ssn_format_stripped else 0)
            | (0x1000 if self.structured_cc_only else 0)
            | (0x2000 if self.alert_broken_media else 0)
        )


class MailConfig(ConfigBase):
    scan_partial_messages: Optional[bool] = Field(default=False)

    def _to_bit_flag(self) -> ctypes.c_uint32:
        return ctypes.c_uint32(0x1 if self.scan_partial_messages else 0)


class DevConfig(ConfigBase):
    collect_sha: Optional[bool] = Field(default=False)
    collect_performance: Optional[bool] = Field(default=False)

    def _to_bit_flag(self) -> ctypes.c_uint32:
        return ctypes.c_uint32(
            0x1 if self.collect_sha else 0 | 0x2 if self.collect_performance else 0
        )


class ScanOptions(ctypes.Structure):
    _fields_ = [
        ("general", ctypes.c_uint32),
        ("parse", ctypes.c_uint32),
        ("heuristic", ctypes.c_uint32),
        ("mail", ctypes.c_uint32),
        ("dev", ctypes.c_uint32),
    ]


class ScanConfig(BaseModel):
    general: GeneralConfig = GeneralConfig()
    parse: ParseConfig = ParseConfig()
    heuristic: HeuristicConfig = HeuristicConfig()
    mail: MailConfig = MailConfig()
    dev: DevConfig = DevConfig()

    def _to_c_struct(self) -> ScanOptions:
        return ScanOptions(
            general=self.general._to_bit_flag(),
            parse=self.parse._to_bit_flag(),
            heuristic=self.heuristic._to_bit_flag(),
            mail=self.mail._to_bit_flag(),
            dev=self.dev._to_bit_flag(),
        )
