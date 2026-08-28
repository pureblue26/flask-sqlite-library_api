"""测试环境配置。"""

from app.core.settings.settings import BaseSettings


class TestSettings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        # DB_NAME/SECRET_KEY 等从 .env.test 读取
