from cdktf import App
from entrypoint import entrypoint
from functions.get_config import get_config

config = get_config("config/config.yml")

app = App()
entrypoint.generate_infrastructure(_config=config, _app=app)
app.synth()