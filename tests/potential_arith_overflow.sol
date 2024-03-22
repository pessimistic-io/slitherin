// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

contract Test {
    uint16 t;

    struct TStruct {
        uint160 xx;
    }

    function decimals16() public returns (uint16) {
        return 10 ** 4;
    }

    /*
        `a` has type `uint64`
        `decimals16()` returns `uint16`
        `x` has type `uint256`
        => Printing warning because mul of uint64 and uint16 may overflow (but casting `a` or the result of `decimals16()` safes from it). 
    */
    function test_vuln1(uint64 a) external {
        uint256 x = a * decimals16();
    }

    function test_vuln2() external returns (uint256 result) {
        uint48 x = 10;
        uint48 y = type(uint48).max;
        uint k = 1;
        result = x * y / k;
    }

    function test_vuln2_wrong_fix() external returns (uint256 result) {
        uint48 x = 10;
        uint48 y = type(uint48).max;
        uint k = 1;
        result = uint256(x * y) / k;
    }

    function test_vuln3() external returns (uint256 result) {
        uint48 x;
        uint32 y;
        result = x + y;
    }

    function test_vuln4() external returns (uint256 result) {
        uint8 x = 10;
        uint8 y = 20;
        result = x ** y;
    }

    function test_vuln5() external returns (uint256) { // @todo handle expression in return statements
        uint8 x = 10;
        uint8 y = 20;
        return x ** y;
    }

    function test_vuln6() external returns (uint256 result) { 
        uint8 x = 10;
        result =  t * x;
    }

    function test_vuln7() external returns (int64 result) { 
        int8 x = 10;
        int32 y;
        result =  y * x + 1;
    }

    function test_vuln8() external returns (int64 result) { 
        int8 x = 10;
        int32 y;
        result =  y * x + 1;

        result = x * y - 10 + 100;

        result = x * y * x * y;
    }

    function test_vuln9() external returns (uint64, uint128) {  // @todo currently we do not handle tuple returns
        uint32 a;
        uint32 b;
        return (a + b, uint128(a) + b);
    }

    function test_vuln10() external returns (uint64) { 
        uint32 a;
        uint32 b;
        return a + b;
    }

    function test_vuln11() external { 
        TStruct memory s = TStruct({xx: 120});
        uint16 a;
        uint32 b;
        s.xx = a + b;
    }

    function test_ok1() external returns (uint128 result) {
        uint128 a;
        uint64 b;
        result = a * b;
    }

    function test_ok2() external returns (uint128) { // @todo handle expression in return statements
        uint128 a;
        uint64 b;
        return a * b;
    }

    function test_ok3() external returns (uint128 result) {
        uint128 a;
        uint64 b;
        uint32 c;
        uint16 d;
        result =  (a * b) / c + d;
    }

    function test_fix_vuln1_ok4(uint64 a) external {
        uint256 x = uint256(a) * decimals16();
    }

    function test_fix_vuln1_slither_bug(uint64 a) external { // @note for some reason slither invokes type incorrectly in this case. So fix need to be applied on the left side of binary expression
        uint256 x = a * uint256(decimals16());
    }

    function test_should_not_trigger(uint64 a) external { // @note for some reason slither
        bytes32 a = bytes32(uint256(1));
        address x = address(uint160(1) + uint160(2));
    }
}