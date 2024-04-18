# @version =0.2.15

@external
@nonreentrant("hello_lock")
def helloWorld() -> String[24]:
    return "Hello World!"

@external
@nonreentrant("another_lock")
def another_reentrant_func() -> uint256:
    return 1

@external
def normal_func() -> uint256:
    return 0