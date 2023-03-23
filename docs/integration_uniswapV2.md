# UniswapV2 Integration

Disabled by default. Use `--detect pess-uni-v2` to enable the detector. 

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
* Recommendation - Put a minReturn parameter of swaps different from max.

### deflationary-token-protection
* Impact - Medium;
* Description - Pools must not allow deflationary (tokens that take fees for transfer) and elastic supply tokens which make arbitrage possible.
* Recommendation - Do not use blacklisted tokens in UniswapV2 integrations.

