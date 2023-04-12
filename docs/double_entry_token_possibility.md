# Double Entry Token Possibility

## Configuration
* Check: `pess-double-entry-token-alert`
* Severity: `High`
* Confidence: `Low` 

## Description
Double-entry token is a token that has two entry points for interactions - a logic contract and a proxy contract.
The detector sees if a contract interacts with double-entry tokens. Such interactions might lead to a contract misfunction.

## Vulnerable Scenario
The vulnerable scenario is in progress.

## Recommendation
A contract must ensure that vulnerabilities related to double token address pointers are not presented.
