# Price Manipulation through token transfers

## Configuration
* Check: `pess-price-manipulation`
* Severity: `High`
* Confidence: `Low`

## Description
The detector finds calculations that depend on the balance and supply of some token. Such calculations could be manipulated through direct transfers to the contract, increasing its balance.

## Vulnerable Scenario
[test scenario](../tests/price_manipulation_test.sol)

## Recommendation
Avoid possible manipulations of calculations because of external transfers.