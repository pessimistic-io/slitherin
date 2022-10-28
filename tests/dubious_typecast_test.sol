pragma solidity ^0.8.0;

contract dubious_typecast_test {

    function getOne () public pure returns (bytes32){
        return bytes32(bytes1(0x01));
    } // actully returns "bytes32: 0x0100000000000000000000000000000000000000000000000000000000000000"


    function number_not_clear () external pure returns (uint8){
        return uint8(uint256(1e18));
    } // actually returns 0
}
