# Curve Readonly Reentrancy

## Configuration

- Check: `pess-curve-readonly-reentrancy`
- Severity: `High`
- Confidence: `Medium`

## Description

Highlights the use of Curve getter functions `get_virtual_price` and `lp_price` (which are not checked for readonly reentrancy `withdraw_admin_fee`), which return values that theoretically could be manipulated during the execution. Details: [Curve LP Oracle Manipulation](https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem/)

## Vulnerable Scenario

[test scenarios](../../tests/curve_readonly_reentrancy_test.sol)

## Related Attacks

- [Jarvis Exploit](https://www.google.com/url?q=https://blog.solidityscan.com/jarvis-polygon-pool-hack-analysis-read-only-re-entrancy-af0607e4585a&sa=D&source=editors&ust=1709713964156907&usg=AOvVaw1Oess2f9Z_UCD6vLM2hN26)
- [Market.xyz Exploit](https://quillaudits.medium.com/decoding-220k-read-only-reentrancy-exploit-quillaudits-30871d728ad5)

## Recomendations

- Verify by calling `withdraw_admin_fee` and checking for fail of call