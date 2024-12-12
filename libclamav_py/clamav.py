import ctypes
import logging
from pathlib import Path

from .config.database import DatabaseConfig
from .config.engine import EngineConfig
from .config.scan import (
    GeneralConfig,
    HeuristicConfig,
    MailConfig,
    ParseConfig,
    ScanConfig,
)


class Client:
    def __init__(
        self,
        *,
        libclamav_path: str = "/opt/lib/libclamav.so",
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        if not Path(libclamav_path).exists():
            raise FileNotFoundError(f"ClamAV library not found: {libclamav_path}")

        self.engine_config = EngineConfig()
        self.scan_config = ScanConfig()
        self.database_config = DatabaseConfig()
        self.logger = logger

        try:
            clamav = ctypes.CDLL(libclamav_path)
            if (ret := clamav.cl_init(ctypes.c_int(0x0))) != 0:
                self.logger.exception(
                    f"Failed to initialize ClamAV: {self.client.cl_strerror(ret)}"
                )
                raise RuntimeError("Failed to initialize ClamAV")
            engine = clamav.cl_engine_new()
            if not engine:
                self.logger.exception(
                    f"Failed to initialize ClamAV: {self.client.cl_strerror(ret)}"
                )
                raise RuntimeError("Failed to initialize ClamAV")
            self.engine = engine
            self.client = clamav
        except Exception as e:
            raise e

    def __del__(self):
        if hasattr(self, "client"):
            self.client.cl_engine_free(self.engine)

    def set_engine_conf(self, config: EngineConfig):
        try:
            for key, value in config.model_dump(by_alias=True).items():
                if isinstance(value, int):
                    self.client.cl_engine_set_num(self.engine, key, value)
                elif isinstance(value, str):
                    self.client.cl_engine_set_str(self.engine, key, value)
                else:
                    raise ValueError(f"Invalid value type: {type(value)}")
        except Exception as e:
            self.logger.exception(f"Failed to set engine configuration: {config}")
            raise e

    def set_database_conf(self, config: DatabaseConfig):
        self.database_config = config

    def set_scan_conf(self, config: ScanConfig):
        self.scan_config = config

    @classmethod
    def from_clamd_conf(
        cls,
        *,
        clamd_conf_path: str,
        libclamav_path: str = "/opt/lib/libclamav.so",
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        try:
            config_dict = {}
            with Path(clamd_conf_path).open() as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, value = line.split(None, 1)
                    if value in ("yes", "true", "1"):
                        value = True
                    elif value in ("no", "false", "0"):
                        value = False
                    config_dict[key] = value
            engine_config = EngineConfig.model_validate(config_dict)
            database_config = DatabaseConfig.model_validate(config_dict)
            scan_config = ScanConfig(
                general=GeneralConfig.model_validate(config_dict),
                parse=ParseConfig.model_validate(config_dict),
                heuristic=HeuristicConfig.model_validate(config_dict),
                mail=MailConfig.model_validate(config_dict),
            )
            client = Client(
                libclamav_path=libclamav_path,
                logger=logger,
            )
            client.set_engine_conf(engine_config)
            client.set_database_conf(database_config)
            client.set_scan_conf(scan_config)
            return client
        except FileNotFoundError as e:
            logger.exception(f"Clamd configuration file not found: {clamd_conf_path}")
            raise Exception from e

    def load_db(self, db_path: str = "/tmp/clamav"):
        if not Path(db_path).exists():
            raise FileNotFoundError(f"ClamAV database not found in: {db_path}")

        sigs = ctypes.c_uint32(0)
        if (
            ret := self.client.cl_load(
                db_path.encode("utf-8"),
                self.engine,
                ctypes.byref(sigs),
                self.database_config._to_bit_flag(),
            )
        ) != 0:
            self.logger.exception(
                f"Failed to load ClamAV database: {self.client.cl_strerror(ret)}"
            )
            self.client.cl_engine_free(self.engine)
            raise RuntimeError("Failed to load ClamAV database")
        if sigs.value == 0:
            self.logger.exception(f"No signatures loaded from {db_path}")
            raise RuntimeError("No signatures loaded")
        self.logger.info(f"Loaded {sigs.value} signatures")

    def compile_engine(self):
        if (ret := self.client.cl_engine_compile(self.engine)) != 0:
            self.logger.exception(
                f"Failed to load ClamAV database: {self.client.cl_strerror(ret)}"
            )
            self.client.cl_engine_free(self.engine)
            raise RuntimeError("Failed to compile ClamAV engine")
        self.logger.info("Compiled ClamAV engine. Ready to scan files")

    def scan_file(self, file_path: str) -> str | None:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        _cl_scan_options = self.scan_config._to_c_struct()
        virname = ctypes.c_char_p()
        scanned = ctypes.c_ulong()
        result = self.client.cl_scanfile(
            file_path.encode("utf-8"),
            ctypes.byref(virname),
            ctypes.byref(scanned),
            self.engine,
            ctypes.byref(_cl_scan_options),
        )
        if result == 0:
            self.logger.info("No virus detected")
            return None
        elif result == 1 and virname.value:
            self.logger.info(f"Virus detected: {virname.value}")
            return virname.value.decode()
        else:
            raise RuntimeError(f"Failed to scan file: {result}")
