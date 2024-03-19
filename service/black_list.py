from redis import Redis

class DenyList:
    def __init__(self, host_name, port):
        self.deny_list = Redis(host=host_name, port=port)
    
    def add_denied_token(self, token, exp):
        self.deny_list.set(token, True, exp)

    def check_denied_token(self, token):
        if not self.deny_list.get(token):
            return False
        return True


def setupDenyList(host_name, port):
    return DenyList(host_name, port)