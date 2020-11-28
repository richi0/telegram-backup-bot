from settings import token, password, file_location, db_logging

def test_env():
    assert len(token) > 1 
    assert type(token) == str
    assert len(password) > 1 
    assert type(password) == str
    assert len(file_location) > 1 
    assert type(file_location) == str
    assert type(db_logging) == bool