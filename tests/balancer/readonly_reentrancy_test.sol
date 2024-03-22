// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;
import {VaultReentrancyLib} from "@balancer-labs/v2-pool-utils/contracts/lib/VaultReentrancyLib.sol";
import "@balancer-labs/v2-interfaces/contracts/vault/IVault.sol";

interface IBalancerPool {
    function getRate() external view returns (uint);
}

contract BalancerIntegration {
    address balancerVault;

    constructor() {}

    function getPriceVulnerable(address vault) public returns (uint) {
        return IBalancerPool(vault).getRate();
    }

    function getPriceVulnerable2(address vault) public {
        bytes32 poolId = "0x123";
        uint256[] memory balances = new uint256[](10);
        (, balances, ) = IVault(balancerVault).getPoolTokens(poolId);
    }

    function _ensureNotReentrant() internal {
        VaultReentrancyLib.ensureNotInVaultContext(IVault(balancerVault));
    }

    function _ensureNotReentrant2() internal {
        IVault(balancerVault).manageUserBalance(new IVault.UserBalanceOp[](0));
    }

    function getPriceOk(address vault) public returns (uint) {
        VaultReentrancyLib.ensureNotInVaultContext(IVault(balancerVault));
        return IBalancerPool(vault).getRate();
    }

    function getPriceOk2(address vault) public returns (uint) {
        _ensureNotReentrant();
        return IBalancerPool(vault).getRate();
    }

    function getPriceOk3(address vault) public returns (uint) {
        _ensureNotReentrant2();
        return IBalancerPool(vault).getRate();
    }

    function getPriceOk4(address vault) public returns (uint) {
        uint a = IBalancerPool(vault).getRate();
        _ensureNotReentrant2();
        return a;
    }

    function getPriceOk5(address vault) public {
        VaultReentrancyLib.ensureNotInVaultContext(IVault(balancerVault));
        bytes32 poolId = "0x123";
        uint256[] memory balances = new uint256[](10);
        (, balances, ) = IVault(balancerVault).getPoolTokens(poolId);
    }
}
