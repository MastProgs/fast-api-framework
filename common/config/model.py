
from common.gmodel import StructModel

class ConfigModel(StructModel):
    pass

# 초기화 필수 & ConfigModel 상속 필수

class ServerConfig(ConfigModel):
    server_name: str = ""
    port: int = 0
    code_generate_before_run: bool = False
    is_chat: bool = False
    
class LogConfig(ConfigModel):
    print_console: bool = True
    print_file: bool = True
    print_stack: bool = True
    print_color: bool = True
    trace_stack_size: int = 10
    log_level: str = "debug"
    
class ContentsDBConfig(ConfigModel):
    db_type: str = ""
    host: str = ""
    port: int = 3306
    name: str = ""
    id: str = ""
    pw: str = ""
    show_log: bool = False
    
class RedisConfig(ConfigModel):
    db_type: str = ""
    host: str = ""
    port: int = 6379
    pw: str = ""
    show_log: bool = False
    
class MongoDBConfig(ConfigModel):
    db_type: str = ""
    host: str = ""
    port: int = 27017
    name: str = ""
    id: str = ""
    pw: str = ""
    show_log: bool = False
    
class JwtToken(ConfigModel):
    access_key: str = ""
    refresh_key: str = ""
    access_expire_min: int = 0
    refresh_expire_day: int = 0