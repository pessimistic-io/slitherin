//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract MinimalTest {
    uint256 private _number;

    function fucntion_public_positive() public view returns (uint256) {
        return _number;
    }

    function fucntion_public_positive2() public view returns (uint256) {
        return _number;
    }

    function fucntion_public_negative() public view returns (uint256) {
        return _number;
    }

    function function_external_negative() external {
        uint256 k = fucntion_public_negative();
    }
}

contract MinimalTest2 {
    uint256 private _number;

    function fucntion_public_positive3() public view returns (uint256) {
        return _number;
    }

    function fucntion_public_negative3() public view returns (uint256) {
        return _number;
    }

    function function_external_negative3() external {
        uint256 k = fucntion_public_negative3();
    }
}
