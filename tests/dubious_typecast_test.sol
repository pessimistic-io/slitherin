pragma solidity ^0.8.0;

contract dubious_typecast_test {
    uint256 constant a = 1000;
    uint8 constant b = 10;

    function mul_vulnerable_uint () public pure returns (uint8){
        uint8 res = uint8(a)*b;
        return res;
    }

    function getOne () public pure returns (bytes32){
        return bytes32(bytes1(0x01));
    } // actully returns "bytes32: 0x0100000000000000000000000000000000000000000000000000000000000000"


    function number_not_clear () external pure returns (uint8){
        return uint8(uint256(1e18));
    } // actually returns 0
}
