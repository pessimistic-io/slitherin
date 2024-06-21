# Curve Vyper Reentrancy

## Configuration

- Check: `pess-vyper-version-reentrancy`
- Severity: `High`
- Confidence: `High`

## Description

Finds if the code is compiled with vulnerable Vyper compiler version and contains non-reentrant modifiers. 
Details:
- [Curve exploit postmortem](https://hackmd.io/@LlamaRisk/BJzSKHNjn)
- [Postmortem from Vyper team](https://hackmd.io/@vyperlang/HJUgNMhs2)

## Vulnerable Scenario

[test scenarios](../../tests/vyper/curve_vyper_reentrancy_test.vy)

## Related Attacks

- [Vyper compiler exploits](https://www.halborn.com/blog/post/explained-the-vyper-bug-hack-july-2023)

## Recomendations

- Upgrade the version of your Vyper compiler.
