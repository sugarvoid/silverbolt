
from bb_lib.user import does_user_exist, create_user


def pass_test():
    return 210


def test_does_user_exist() -> None:
    assert(does_user_exist('000000000'))

def test_create_user() -> None:
    print("create funtion")
    assert(pass_test(), 201)

def test_delete_user() -> None:
    print("delete function")
    assert(3, 3)

def test_add_user() -> None:
    pass

def test_logger() -> None:
    # make log post
    # check if last last == the test post
    # delete last line
    pass

def test_() -> None:
    # 
    # 
    # 
    pass