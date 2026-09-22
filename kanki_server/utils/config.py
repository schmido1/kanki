from confz import BaseConfig, FileSource
from pydase.config import ServiceConfig


class KankiServiceConfig(BaseConfig):
    host: str
    web_port: int
    generate_web_settings: bool
    print(ServiceConfig().config_dir)
    CONFIG_SOURCES = FileSource(file=ServiceConfig().config_dir / "service_config.yaml")
