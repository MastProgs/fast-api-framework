from common.gmodel import Req_WebPacketProtocol, Res_WebPacketProtocol, WebPacketProtocol
from common.enums import ErrorType, HandlerTopic

class BetProtocol_Request(Req_WebPacketProtocol):
    topic: int = HandlerTopic.NONE.value
    pass

class BetProtocol_Response(Res_WebPacketProtocol):
    topic: int = HandlerTopic.NONE.value
    pass


###################### Bet Server Protocol Start ######################

class Req_LoginBetServer(BetProtocol_Request):
    pass

class Res_LoginBetServer(BetProtocol_Response):
    
    def __init__(self):
        super().__init__()
        self.topic = HandlerTopic.BET_LOGIN.value
        
    pass