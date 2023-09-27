# UniswapV2 Integration

Looks for contracts inheritance. Use `--detect pess-uni-v2` to forcefully enable the detector. 

## Configuration
* Check: `pess-uni-v2`
* Confidence: `Medium`

## Description
Checks the correctness of UniswapV2 integration in the contract. 

## Detectors
### pair-balance-is-used
* Impact - High;
* Description - The pair balance value (or its' change) can be manipulated with a flashloan or a cyclical swap path.
* Recommendation - Do not rely directly on the pair balance value.

### pair-reserve-is-used
* Impact - High;
* Description - The pair reserve value (or its' change) can be manipulated with a flashloan or a cyclical swap path.
* Recommendation - Do not rely directly on the pair balance value.

### pair-is-used
* Impact - Medium;
* Description - The protocol is secured with the Router contract. The direct usage of the Pair is dangerous due to its complexity.
* Recommendation - Use the Router contract instead of using the Pair contract directly.

### swap-minReturn-is-zero
* Impact - Medium;
* Description - All swaps must not have parameter minReturn equal to 0.
* Recommendation - Put a minReturn parameter of swaps different from 0.

### swap-maxReturn-is-infinite
* Impact - Medium;
* Description - All swaps must not have parameter maxReturn equal to max.
* Recommendation - Put a maxReturn parameter of swaps different from max.

### deflationary-token-protection
* Impact - Medium;
* Description - Pools must not allow deflationary (tokens that take fees for transfer) and elastic supply tokens which make arbitrage possible.
* Recommendation - Do not use [deflationary](../utils/deflat_tokens.json) and [rebase](../utils/rebase_tokens.json) tokens in UniswapV2 integrations.

### tainted-swap-routes
* Impact - Medium;
* Description - Looks for UniV2 funtions where the path parameter is partially or entirely provided from external invocation.
* Recommendation - Do not use functions where path parameter is provided through customs invocations.

## Vulnerable Scenario
[test scenario](../tests/Bad_UniswapV2_test.sol)
