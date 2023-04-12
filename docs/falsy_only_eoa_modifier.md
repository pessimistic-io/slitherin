# Falsy Only EOA Modifier

## Configuration
* Check: `pess-only-eoa-check`
* Severity: `Medium`
* Confidence: `Low`

## Description
The detector highlights the `msg.sender == tx.origin` statements.
From a design standpoint, contracts should work correctly independently of the calling account. 
Any EoA check is a hack and should be avoided.
Indeed, tx.origin/msg.sender check protects against some types of attacks (most notably, re-entrancy and flashloans). However, other attacks usually performed via smart contracts can be executed from an EoA. For example, weak random can be exploited with a MEV bundle.

## Vulnerable Scenario
[test scenario](../tests/falsy_only_eoa_modifier_test.sol)

## Recommendation
Refrain from relying on EoA checks for security. Instead, design your project to interact with other contracts safely. Ensure that your contracts are not vulnerable to re-entrancy, flashloans, or weak random attacks.