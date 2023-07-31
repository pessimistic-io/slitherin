pragma solidity ^0.8.0;

contract dubious_typecast_test {
    function getOne() public pure returns (bytes32) {
        return bytes32(bytes1(0x01));
    } // actully returns "bytes32: 0x0100000000000000000000000000000000000000000000000000000000000000"

    function number_not_clear() external pure returns (uint8) {
        uint t = 256;
        uint8 k = uint8(t); //new:this is dubious
        return uint8(uint256(1e18));
    } // actually returns 0

    function _approve(
        address owner,
        address spender,
        uint256 amount
    ) internal virtual {}

    function address_castNotvulnerable() external returns (address) {
        dubious_typecast_test d;
        _approve(address(this), address(d), 0); //new:this is FP

        return address(d);
    } // actually returns 0
}
