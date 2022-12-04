import os
from dotenv import load_dotenv

class OSUtil:
    default_prod_env = os.path.join(os.getcwd(),".prodenv")

    @classmethod
    def load_env(cls, env_file):
        assert os.path.exists(env_file)
        load_dotenv(dotenv_path=env_file)