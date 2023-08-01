pragma solidity ^0.8.18;

contract Target{

  function positive(uint256 inp) public returns (uint256) {
    for (uint256 i; i < 10; ) {
      if (inp < 2) {
        continue;
      }
      /* logic */
      unchecked {
        ++i;
      }
    }
    return 0;
  }

  function negative(uint256 inp) public returns (uint256) {
    for (uint256 i; i < 10; ) {
      unchecked {
        ++i;
      }
      if (inp < 2) {
        continue;
      }
      /* logic */
    }
    return 0;
  }

  /*

  Hit live on chain: bulkRegister(), bulkWithdraw()  https://etherscan.io/address/0xeb9014610d4daC128f9DA00C397Ce9119Ee777F5


  Hit from a Sherlock audit: https://github.com/sherlock-audit/2023-02-olympus/blob/main/src/policies/lending/WstethLiquidityVault.sol#L192-L216

  function _accumulateExternalRewards() internal override returns (uint256[] memory) {
    uint256 numExternalRewards = externalRewardTokens.length;

    auraPool.rewardsPool.getReward(address(this), true);

    uint256[] memory rewards = new uint256[](numExternalRewards);
    for (uint256 i; i < numExternalRewards; ) {
      ExternalRewardToken storage rewardToken = externalRewardTokens[i];
      uint256 newBalance = ERC20(rewardToken.token).balanceOf(address(this));

      // This shouldn't happen but adding a sanity check in case
      if (newBalance < rewardToken.lastBalance) {
        emit LiquidityVault_ExternalAccumulationError(rewardToken.token);
        continue;
      }

      rewards[i] = newBalance - rewardToken.lastBalance;
      rewardToken.lastBalance = newBalance;

      unchecked {
        ++i;
      }
    }
    return rewards;
  }
   */

}