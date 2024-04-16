interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
}
contract Test1 {
    IERC20 token;

    function test_vuln_1() external returns(uint256 price) {
        price = token.balanceOf(address(this)) / token.totalSupply();
    }

    function test_vuln_2() external returns(uint256 price) {
        uint256 bal = token.balanceOf(address(this));
        uint256 supply = token.totalSupply();
        price = bal / supply; 
    }

    function test_vuln_3() external returns(uint256 price) {
        uint256 bal = getBalance();
        price = bal / token.totalSupply();
    }

    function test_vuln_4() external returns(uint256 price) {
        uint256 bal = getBalance();
        price = 10 + (bal / (token.totalSupply() * 5));
    }

    function test_vuln_5() external returns(uint256 price) {
        price = getBalance() / mySupply();
    }

    function test_vuln_6() external returns(uint256 price) {
        price = getBalance() + mySupply() + 1;
    }

    function getBalance() public returns(uint256 bal) {
        bal = token.balanceOf(msg.sender);
    }

    function mySupply() public returns (uint256) {
        return 100;
    }
}