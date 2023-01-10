
from common.gmodel import StructModel

class ConfigModel(StructModel):
    pass

# 초기화 필수 & ConfigModel 상속 필수

class ServerConfig(ConfigModel):
    server_name: str = ""
    port: int = 0
    code_generate_before_run: bool = False
    
class LogConfig(ConfigModel):
    print_console: bool = True
    print_file: bool = True
    print_stack: bool = True
    print_color: bool = True
    trace_stack_size: int = 10
    log_level: str = "debug"
    
class ContentsDBConfig(ConfigModel):
    db_type: str = ""
    port: int = 0
    host: str = ""
    name: str = ""
    id: str = ""
    pw: str = ""
    show_log: bool = False
    
class LogDBConfig(ConfigModel):
    db_type: str = ""
    port: int = 0
    host: str = ""
    name: str = ""
    id: str = ""
    pw: str = ""
    show_log: bool = False
    
class JwtToken(ConfigModel):
    access_key: str = ""
    refresh_key: str = ""