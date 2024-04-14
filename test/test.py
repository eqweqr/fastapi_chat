from fastapi.testclient import TestClient
from main import app, make_migrations, make_downgrade
import pytest
import time

client = TestClient(app)
   

@pytest.fixture(scope='class')
def init_db():
    make_migrations()
    time.sleep(3)
    yield
    make_downgrade()


@pytest.fixture(scope='function')
def register(username, email, password, first, init_db):
    response = None
    if first:
        response = client.post('/register',
                                data={'username': username, 'email': email, 'password': password},
                                headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    yield response


@pytest.fixture(scope='function')
def login(register, log_user, log_pass):
    response = client.post('/login',
                            data={'username': log_user, 'password': log_pass},
                            headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    yield response


class TestRegistration:

    @pytest.mark.parametrize('username,password,email,first,status,length',
                         [
                            ('astarot', 'password', 'astartes@mail.ru', True, 201, True),
                            ('marin', 'pasworder', 'astartes@mail.ru', True, 409, False),
                            ('astarot', 'password', 'hh@mail.ru', True, 409, False),
                            ('azazel', 'pass', 'fsa@.u', True, 409, False), 
                            ('azazel', 'pass', 'fsa@google.com', True, 201, True),
                         ])
    def test_register_new_user(self, register, status, length):
        assert register.status_code == status
        assert (len(register.json().get('hashed_username', '')) > 0) is length
    

class TestConfirm:

    @pytest.mark.parametrize('unhashed,username,password,email,first,hash,status',[
        ('astarot', 'astarot', 'password', 'astartes@mail.ru', True, '', 201),
        ('astarot', 'astarot', 'password', 'astartes@mail.ru', False, 'fsdaf', 401)
    ])
    def test_confirm(self, unhashed, hash, status, register):
        if len(hash)==0:
            hash = register.json().get('hashed_username')
        resp = client.patch(f'/confirm/{unhashed}/?hashed={hash}')
        assert resp.status_code == status


class TestLogin:

    @pytest.mark.parametrize('username,password,email,first,log_user,log_pass,status_code',
                        [
                            ('astarot', 'password', 'astartes@mail.ru', True, 'astarot', 'password', 200),
                            ('', '', '', False, 'astartes', 'password', 409),
                            ('', '', '', False, 'astarot', 'password1', 409)
                        ])
    def test_login(self, login, status_code):
        assert login.status_code == status_code
        if status_code == 200:
            assert login.json().get('access_token')
            assert login.json().get('refresh_token')


class TestRefresh:

    @pytest.mark.parametrize('username,password,email,first,log_user,log_pass,status_code,token,grant_type,user_agent',
                            [ 
                                ('astarot', 'password', 'astartes@mail.ru', True, 'astarot', 'password', 200, '', 'refresh_token', ''),
                                ('', '', '', False, 'astarot', 'password', 409, 'rweaxd23', 'refresh_token', ''),
                                ('', '', '', False, 'astarot', 'password', 401, '', 'grant', ''),
                                ('', '', '', False, 'astarot', 'password', 409, '', 'refresh_token', 'Default')
                            ])
    def test_refresh_token(self, login, status_code, token, grant_type, user_agent):
        refresh_token = login.json().get('refresh_token')
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if len(user_agent) != 0:
            headers.update({'User-Agent': user_agent})
        if len(token) != 0:
            refresh_token = token
        req = client.post('/refresh',
                data={'grant_type': grant_type, 'refresh_token': refresh_token},
                headers=headers
            )
        assert req.status_code == status_code 
        if req.status_code == 200:
            assert req.json().get('username')
            assert req.json().get('access_token')
        

class TestLogout:

    @pytest.mark.parametrize('username,password,email,first,log_user,log_pass,status_code,token,grant_type,user_agent',
                            [ 
                                ('astarot', 'password', 'astartes@mail.ru', True, 'astarot', 'password', 200, '', 'refresh_token', ''),
                                ('', '', '', False, 'astarot', 'password', 409, 'rweaxd23', 'grant', ''),
                                # ('', '', '', False, 'astarot', 'password', 409, '', 'grant', ''),
                                # ('', '', '', False, 'astarot', 'password', 409, '', 'refresh_token', 'Default')
                            ])
    def test_logout(self, login, status_code, token, grant_type, user_agent):
        refresh_token = login.json().get('refresh_token')

        if len(token) != 0:
            refresh_token = token

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        req = client.post('/logout',
                data={'grant_type': grant_type, 'refresh_token': refresh_token},
                headers=headers
        )
        assert req.status_code == status_code
        if req.status_code == 200:
            req = client.post('/refresh',
                data={'grant_type': grant_type, 'refresh_token': refresh_token},
                headers=headers
            )
            assert req.status_code == 409
        
        # assert req.status_code == status_code 
        # if req.status_code == 200:
        #     assert req.json().get('username')
        #     assert req.json().get('access_token')

