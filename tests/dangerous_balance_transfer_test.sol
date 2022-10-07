/*
Warning! The code is not production ready. It is provided for educational purposes only.
*/

pragma solidity ^0.8.0;

contract ERC20 {
    mapping(address => uint256) balances;

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
    //relations are not done yet
    function transfer_vuln2(address to) public returns(bool){
        uint256 balance = balanceOf(address(this));
        return transfer(to, balance);
    }

    function transfer_ok(address to, uint256 amount) public returns(bool){
        return transfer(to, amount);
    }
}