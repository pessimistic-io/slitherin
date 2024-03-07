// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

interface ICurveLP {
    function get_virtual_price() external returns (uint256);
    function withdraw_admin_fee() external returns (uint256);
}

contract CurveLPTest {
    ICurveLP lp = ICurveLP(address(0x0));

    function vuln () external {
        uint p = lp.get_virtual_price();
    }
    function _ensureNonReentrant() private {
        (bool success,) = address(lp).call(abi.encodeWithSelector(ICurveLP.withdraw_admin_fee.selector));
        require(!success, "reentrant call");
    }
    function ok() external {
        _ensureNonReentrant();
        uint p = lp.get_virtual_price();
    }
}