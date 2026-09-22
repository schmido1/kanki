from pydase import Server
from pydase.config import ServiceConfig

from .utils.config import KankiServiceConfig
from .kanki import Kanki

service = Kanki()

Server(
    service=service,
    css=ServiceConfig().config_dir / "custom.css",
    web_port=KankiServiceConfig().web_port,
    host=KankiServiceConfig().host,
    generate_web_settings=KankiServiceConfig().generate_web_settings,
).run()
