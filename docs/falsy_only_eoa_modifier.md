# Falsy Only EOA Modifier

## Configuration
* Check: `only-eoa-check`
* Severity: `Medium`
* Confidence: `High`

## Description
Highlights the `msg.sender == tx.origin` statements.
From design standpoint, contracts should work correctly independently of the calling account. 
Any EoA check is a hack and should be avoided.
Indeed, tx.origin/msg.sender check protects against some types of attacks (most notably, re-entrancy and flash loans). However, other attacks that are usually performed via smart contracts can be executed from an EoA. For example, weak random can be exploited with a MEV bundle.

## Exploit Scenario
[Exploit]()

## Recommendation
Don't rely on EoA checks for security. Instead, design your project so that they can safely interact with other contracts. Make sure, that your contracts are not vulnerable to re-entrancy, flash loans, weak random attacks.