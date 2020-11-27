from settings import token, password

def test_env():
    assert len(token) > 1 
    assert type(token) == str
    assert len(password) > 1 
    assert type(password) == str