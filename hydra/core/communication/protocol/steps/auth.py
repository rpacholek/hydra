from ..base import *
from ..exceptions import *

from ....environment import NodeType

class PlainAuth:
    def __init__(self):
        pass

    def authenticate(self, *, user="", password="", **kwargs):
        print(user, password)
        if user == "user" and password == "password":
            return True
        return False

class AuthStatus(enum.Enum):
    Success = 0
    Failed = 1
    Init = 2
    Waiting = 3


class AuthenticationProtocol(ProtocolStep):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authetication = {"plain": PlainAuth()}
        self.local_state = AuthStatus.Init # If remote auth localy
        self.remote_state = AuthStatus.Init # If local auth remotely

        if self.local_env.get_node_type() == NodeType.Supervisor:
            self.methods = "plain"
        else:
            self.methods = "none"
            self.local_state = AuthStatus.Success

    def init(self):
        self.send(self.m_auth_type())

    def receive(self, message):
        info = message.get_info()
        if info["stage"] == "init":
            print("Auth:init")
            if info["methods"] == "plain":
                self.send(self.m_auth_user(info["methods"]))
                self.remote_state = AuthStatus.Waiting
            else:
                self.remote_state = AuthStatus.Success
        elif info["stage"] == "auth":
            print("Auth:auth")
            # TODO: Switch to walrus opertator whenever 3.8
            auth = self.authetication.get(info["method"])
            if auth and auth.authenticate(**info):
                self.local_state = AuthStatus.Success
                self.send(self.m_auth_result(True))
            else:
                self.local_state = AuthStatus.Failed
                self.send(self.m_auth_result(False))
        elif info["stage"] == "result":
            auth = "authenticated"
            if auth in info and info[auth]:
                print("Auth:result:success")
                self.remote_state = AuthStatus.Success
            else:
                print("Auth:result:failed")
                self.remote_state = AuthStatus.Failed
        self.try_ending()

    def try_ending(self):
        if self.local_state == AuthStatus.Success and self.remote_state == AuthStatus.Success:
            self.finish()
        elif self.remote_state == AuthStatus.Failed or self.remote_state == AuthStatus.Failed:
            self.failed()
        # else: Wait for action

    def m_auth_type(self):
        return ProtocolMessage({
            "stage": "init",
            "methods": self.methods
            })

    def m_auth_user(self, method):
        return ProtocolMessage({
            "stage": "auth",
            "method": "plain",
            "user": "user",
            "password": "password"
            })

    def m_auth_result(self, result):
        return ProtocolMessage({
            "stage": "result",
            "authenticated": result
            })


