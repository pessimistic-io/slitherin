/*
Warning! The code is not production ready. It is provided for educational purposes only.
*/
pragma solidity ^0.8.0;
import "./interfaces/IERC20.sol";

contract DangerousERC20 {
    mapping(address => uint256) balances;
    bool isProtected = true;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    event Transfer(address indexed from, address indexed to, uint256 value);                

    function balanceOf(address owner) public view returns(uint256) {
        return balances[owner];
    }

    function transfer(address to, uint256 value) public returns(bool) {
        balances[to] += value;
        balances[msg.sender] -= value;
        emit Transfer(msg.sender, to, value);
        return true;
    }


    //test functions
    function transfer_vuln(address to) public returns(bool){
        return transfer(to, balanceOf(address(this)));
    }

    function transfer_vuln2(address to, uint256 amount) public returns(bool){
        return transfer(to, amount);
    }

    function transfer_ok(address to, uint256 amount) public onlyOwner returns(bool){
        return transfer(to, amount);
    }
}

contract dangerous_balance_transfer_test {
    IERC20 token;

    function transfer_vuln3(address to, uint256 amount) public {
        token.transfer(to, amount);
    }
}