from redis import Redis


class DenyList:
    """
        Add all refresh token in memory db -- Redis. If user logout
    or try to use refresh token with different fingerprint, delete
    token.
    """
    def __init__(self, host_name, port):
        """
            Collection of valid refresh token. With fingerprint.
        Refresh token will be deleted on expire
        """
        self.all_current_tokens = Redis(host=host_name, port=port)
    

    def add_refresh_token(self, token, value, exp):
        """
            Add refresh token on login.    
        """
        self.all_current_tokens.set(token, value, exp)

    def delete_refresh_token(self, token):
        """
            Delete refresh token when user logout, or if try to
        refresh with different fingerprint.
        """
        self.all_current_tokens.delete(token)

    def get_token_fingerprint(self, token):
        """
            Get current fingerprint of token
        """
        return self.all_current_tokens.get(token)



def setupDenyList(host_name, port):
    return DenyList(host_name, port)