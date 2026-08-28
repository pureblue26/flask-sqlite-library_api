"""开发环境配置。"""

from app.core.settings.settings import BaseSettings


class DevSettings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        # DB_NAME 等从 .env.dev 读取（继承 BaseSettings.__init__）
