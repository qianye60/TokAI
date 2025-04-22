from sqlite.dbconfig import get_session
from model.config_model import Config
from sqlmodel import select

async def get_config():
    try:
        Session = next(get_session())
        result = Session.exec(select(Config))
        config = result.first()
        if not config:
            return Config()
        return config
    except Exception as e:
        print(f"配置错误: {str(e)}")
        return Config()

async def update_config(config: Config):
    try:
        Session = next(get_session())
        # 获取第一个配置项，而不是整个列表
        result = Session.exec(select(Config))
        config_db = result.first()
        
        if config_db:
            # 更新现有配置
            config_db.title = config.title
            config_db.email_register = config.email_register
            config_db.guest = config.guest
            config_db.default_money = config.default_money
            Session.add(config_db)
        else:
            return False
        Session.commit()
        return True
    except Exception as e:
        print(f"配置错误: {str(e)}")
        return False
