#三方库
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import secrets
#——————————————————————————————————————————全局配置—————————————————————————————————————————————


#登录持续天数
ACCESS_TOKEN_EXPIRE_DAYS = 7
#全局密钥
SECRET_KEY = secrets.token_hex(32)  # 生成随机的32字节密钥

#加密算法
ALGORITHM = "HS256"
if not SECRET_KEY:
    print("警告：未设置 SECRET_KEY 环境变量！将使用默认的不安全密钥。")
    # 在实际应用中，你可能想抛出错误或退出
    # 为了演示/本地开发，如果需要可以生成一个临时的，但要大声警告。
    # SECRET_KEY = secrets.token_urlsafe(32) # 不要在生产环境中通过代码这样做
    raise ValueError("必须提供 SECRET_KEY 环境变量！")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



#验证用户密码是否与数据库哈希密码匹配
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#密码加密哈希
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#认证用户存在且账号密码正确
def authenticate_user(user_db, password: str):
    if not verify_password(password, user_db.hashed_password):
        return False
    return user_db

#创建令牌
def create_access_token(data: dict,token_expire: timedelta | None = None):
    to_encode = data.copy()
    if token_expire:
        expire = datetime.now(timezone.utc) + token_expire
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)



