from redis import Redis


class DenyList:
    """instead collection denied token, db contains active token,
    if was compromied just del it from db."""
    def __init__(self, host_name, port):
        self.all_current_tokens = Redis(host=host_name, port=port)
    

    """value is ip and useragent, if have token with same ip and user-agent, drop token"""
    def add_denied_token(self, token, exp, value):
        self.all_current_tokens.set(token, value, exp)

    def check_denied_token(self, token):
        value = self.all_current_tokens.get(token)
        return value


def setupDenyList(host_name, port):
    return DenyList(host_name, port)