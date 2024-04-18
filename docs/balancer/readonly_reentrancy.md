# Balancer Readonly Reentrancy

## Configuration

- Check: `pess-balancer-readonly-reentrancy`
- Severity: `High`
- Confidence: `Medium`

## Description

Highlights the use of Balancer getter functions `getRate` and `getPoolTokens` (which are not checked for readonly reentrancy via `VaultReentrancyLib.ensureNotInVaultContext` or `IVault.manageUserBalance`), which return values that theoretically could be manipulated during the execution.

## Vulnerable Scenario

[test scenarios](../../tests/balancer/readonly_reentrancy_test.sol)

## Related Attacks

- [Sentimentxyz Exploit](https://quillaudits.medium.com/decoding-sentiment-protocols-1-million-exploit-quillaudits-f36bee77d376)
- [Sturdy Exploit](https://blog.solidityscan.com/sturdy-finance-hack-analysis-bd8605cd2956)

## Recommendation

- [Official Balancer recomendation](https://docs.balancer.fi/concepts/advanced/valuing-bpt/valuing-bpt.html#on-chain-price-evaluation)
