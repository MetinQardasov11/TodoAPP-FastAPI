from codecs import ascii_encode
import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1
    
    

def test_is_instance():
    assert isinstance(1, int)
    assert not isinstance(1, str)
    assert isinstance('Hello World', str)
    
    
def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False
    
    
def test_type():
    assert type('Hello' is str)
    assert type('World' is not int)
    
    
    
def test_greater_and_less_than():
    assert 1 > 0
    assert 1 < 2
    
    
    
def test_list():
    num_list = [1, 2, 3, 4, 5]
    bool_true_list = [True, True]
    bool_false_list = [False, False]
    assert 3 in num_list
    assert True in bool_true_list
    assert all(bool_true_list)
    assert any(bool_true_list)
    assert not any(bool_false_list)
    
    
    
class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
        
        
@pytest.fixture
def employee():
    return Student('Metin', 'Qardasov', 'Computer Science', 3)


def test_person_initilization(employee):
    assert employee.first_name == 'Metin', 'First name should be Metin'
    assert employee.last_name == 'Qardasov', 'Last name should be Qardasov'
    assert employee.major == 'Computer Science', 'Major should be Computer Science'
    assert employee.years == 3, 'Year should be 3'