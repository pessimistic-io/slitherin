# Tx Gasprice Warning

## Configuration
* Check: `pess-tx-gasprice`
* Severity: `High`
* Confidence: `Low`

## Description
tx.gasprice variable is set by contract users not developers. The detector sees if a contract uses tx.gasprice variable.

## Vulnerable Scenario
[test scenario](../tests/tx_gasprice_warning_test.sol)

## Related Attack

[Ethereum-alarm-clock Exploit](https://cointelegraph.com/news/ethereum-alarm-clock-exploit-leads-to-260k-in-stolen-gas-fees-so-far)

## Recommendation
Make sure that exploits with tx.gasprice variable set by users are not possible.
