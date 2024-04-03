import pytest
from model.db import add_user
from customlog import custom_logger
from model.db import atomic_session, confirm_email, get_user
from model.migration import get_alembic_config, run_upgrade, run_downgrade




@pytest.fixture()
def atomic_session_decorator():
    cfg = get_alembic_config()
    run_upgrade(cfg)
    print('run')
    yield
    run_downgrade(cfg)
    
# exceptions = [Exception, ZeroDivisionError]
    
# @pytest.mark.xfail
def test_user_adding(atomic_session_decorator):
    test_cases = [
        {
            'status': 'OK',
            'exception_message': '',
            'username': 'Jone',
            'hashed_password': '1eqer3fs',
            'email': 'qwer@mail.ru',
            'activated': False,
        },
        {
            'status': 'Fail. Invalid email',
            'exception_message': 'incorrect email format',
            'username': 'Jone',
            'hashed_password': '1eqer3fs',
            'email': 'qwermail.ru',
            'activated': False,

        },
        {
            'status': 'Fail. Same email',
            'exception_message': 'complicated',
            'username': 'Jone',
            'hashed_password': '1eqer3fs',
            'email': 'qwer@mail.ru',
            'activated': False,
        }
    ]
    for tc in test_cases:
        if not tc['exception_message']:
            add_user(username=tc['username'], email=tc['email'],
                     hashed_password=tc['hashed_password'])
        else:
            if tc['exception_message'] == 'complicated':
                with pytest.raises(Exception):
                    add_user(username=tc['username'], email=tc['email'],
                        hashed_password=tc['hashed_password']) 
            else:  
                with pytest.raises(Exception, match=tc['exception_message']):
                    add_user(username=tc['username'], email=tc['email'],
                        hashed_password=tc['hashed_password'])
