// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

import "../node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DoubleEntryTokenTest_vuln {
    function vulnerable(IERC20[] calldata tokens0, address[] calldata tokens1) external {
        for (uint256 i = 0; i < tokens0.length; i++){
            uint256 bal = tokens0[i].balanceOf(address(this));
            tokens0[i].transfer(tokens1[i], bal);
        }
    }

    function not_vulnerable(address[] calldata users) view external returns(uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < users.length; i++){
            total += payable(users[i]).balance;
        }
        return total;
    }

    /**
     * @dev Extracted from the Openzeppelin Governor contract as an example 
     * https://github.com/OpenZeppelin/openzeppelin-contracts/blob/f347b410cf6aeeaaf5197e1fece139c793c03b2b/contracts/governance/Governor.sol#L414)
     */
    function _afterExecute(
        uint256 /* proposalId */,
        address[] memory /* targets */,
        uint256[] memory /* values */,
        bytes[] memory /* calldatas */,
        bytes32 /*descriptionHash*/
    ) internal virtual {
        // if (_executor() != address(this)) {
        //     if (!_governanceCall.empty()) {
        //         _governanceCall.clear();
        //     }
        // }
    }
}