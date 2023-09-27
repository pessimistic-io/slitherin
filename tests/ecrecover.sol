// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

contract EcrecoverTest {
    mapping(address => uint) balances;

    function ecrecover_positive() external {
        address signer = ecrecover("", 0, 0, 0);
    }

    function ecrecover_positive2() external {
        address signer = ecrecover("", 0, 0, 0);
        require(balances[signer] > 0);
        assert(balances[signer] > 0);
    }

    function ecrecover_negative() external {
        address signer = ecrecover("", 0, 0, 0);
        require(signer != address(0x0), "oops");
    }

    function ecrecover_negative2() external {
        address signer = ecrecover("", 0, 0, 0);
        assert(signer != address(0));
    }

    function ecrecover_negative3() external {
        address signer = ecrecover("", 0, 0, 0);
        if (signer == address(0)) {
            revert("smth");
        }
    }
}
