"""生产环境配置。"""

from app.core.settings.settings import BaseSettings


class ProdSettings(BaseSettings):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        # 所有值（SECRET_KEY/DB_*）从 .env.prod 读取
        # SECRET_KEY 无默认值 → 缺失时 self.SECRET_KEY 为 None，启动校验失败
