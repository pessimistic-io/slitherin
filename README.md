# Slitherin by Pessimistic.io

[![Blog](https://img.shields.io/badge/Blog-Link-blue?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](https://blog.pessimistic.io/)
[![Our Website](https://img.shields.io/badge/By-pessimistic.io-green?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](https://pessimistic.io/)
[![Mail](https://img.shields.io/badge/Mail-gm%40pessimistic.io-orange?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](mailto:gm@pessimistic.io)

**Welcome!** We are the [pessimistic.io](https://pessimistic.io/) team, and in recent months we have been actively developing our [own **Slither detectors**](https://github.com/pessimistic-io/slitherin/tree/develop/slitherin/detectors) to help with code review and audit process. This repository contains everything you may require to work with them!

We increased the sensitivity of our detectors since they are *quite straightforward* and not written in the "original style." As a result, they produce FPs ([False Positives](https://en.wikipedia.org/wiki/False_positives_and_false_negatives)) more frequently than original ones. So that, our detectors are a kind of automation of the checks implemented in the checklist, their main purpose is to look for issues and assist the code auditor.

Please let us know if you have discovered an [issue/bug/vulnerability](https://telegra.ph/BountyCTF-Platforms-Web3-04-19) via our custom Slither detectors. You may contact us via opening a [PR/Issue](https://github.com/pessimistic-io/slitherin/issues) or [directly](mailto:gm@pessimistic.io), whichever is more convenient for you. If you have any further questions or suggestions, please [join our Discord Server](https://discord.gg/vPxkR8B9p7) or [Telegram chat](https://t.me/+G96ejJ7Pmgk1NDZi)! We hope to see you there, and we intend to support the community and its initiatives!

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/+t8dRfLLbVx1iYzNi)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/vPxkR8B9p7)

## Repository Navigation

#### **Table of Contents:**

| Section                      | Link                                                                                                          |
|------------------------------|---------------------------------------------------------------------------------------------------------------|
| Docs                         | [Docs for each detector](https://github.com/pessimistic-io/slitherin/tree/master/docs)                        |
| Slitherin                    | [Detectors code](https://github.com/pessimistic-io/slitherin/tree/master/slitherin/detectors)                 |
| Tests                        | [Test contracts for detectors](https://github.com/pessimistic-io/slitherin/tree/master/tests)                 |
| Utils                        | [Auxiliary files](https://github.com/pessimistic-io/slitherin/tree/master/slitherin/utils)                    |
| Issues                       | [Suggest an idea](https://github.com/pessimistic-io/slitherin/issues)                                         |
| Installation Process         | [Step-by-Step guide](https://github.com/pessimistic-io/slitherin#installation-process)                        |
| Detectors                    | [Detectors table](https://github.com/pessimistic-io/slitherin#detectors-table)                                |
| Enhancements & New Detectors | [Project Improvements](https://github.com/pessimistic-io/slitherin#enhancements--new-detectors)               |

## Installation Process
### Using Git
To install Pessimistic Detectors: 
1. Install the [original Slither](https://github.com/crytic/slither#how-to-install);
2. Clone our repository;
3. Run the following command in our repository folder to add new detectors to Slither:
```bash
python3 setup.py develop
```
> Keep in mind that you don't have to reinstall the plugin after changes in the repository!
4. Dependencies must be installed in order to test the detectors on our test contracts:
```bash
npm install
```
### Using Pip
1. Install the [original Slither](https://github.com/crytic/slither#how-to-install);
2. Install the pip [package](https://pypi.org/project/slitherin/):
```bash
pip install slitherin
```

## Usage
### Slitherin-cli (Recommended)
Use Slitherin-cli to run detectors on a Hardhat/Foundry/Dapp/Brownie application. You have the following options:
* Run ONLY Slitherin detectors:
```bash
slitherin . --pess
```
* Run ONLY Slither detectors:
```bash
slitherin . --slither
```
* Run Slither detectors, then Slitherin detectors:
```bash
slitherin . --separated
```
* Run Arbitrum-specific Slitherin detectors:
```bash
slitherin . --arbitrum
```
> Keep in mind that Slitherin-cli supports all Slither run options.
### Slither
Slitherin detectors are included into original Slither after the installation. You can use Slither [as usual](https://github.com/crytic/slither#usage).

## **Detectors Table**

| Detector Link                                                                                                                                             | Docs & Setup                                                                                                     | Test Contract                                                                                                                                             | Valid* Issues                                                                                                    |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| [Unprotected Setter](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/unprotected_setter.py)                                | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/unprotected_setter.md)                    | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/unprotected_setter_test.sol)                                                                                                                                               | 1                                                                                                                |
| [Unprotected Initialize](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/unprotected_initialize.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/unprotected_initialize.md)                | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/unprotected_initialize_test.sol)                                                     | 0                                                                                                                |
| [TX Gasprice Warning](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/tx_gasprice_warning.py)                              | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/tx_gasprice_warning.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/tx_gasprice_warning_test.sol)                                                        | 0                                                                                                                |
| [UniswapV2 Integration](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/uni_v2.py)                                         | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/integration_uniswapV2.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/Bad_UniswapV2_test.sol)                                                              | 0                                                                                                                |
| [Token Fallback](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/token_fallback.py)                                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/token_fallback.md)                        | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/token_fallback_test.sol)                                                             | 0                                                                                                                |
| [Timelock Controller](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/timelock_controller.py)                              | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/timelock_controller.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/timelock_controller_test.sol)                                                        | 1                                                                                                                |
| [Strange Setter](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/strange_setter.py)                                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/strange_setter.md)                        | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/strange_setter_test.sol)                                                             | 0                                                                                                                |
| [Read-only Reentrancy](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/read_only_reentrancy.py)                            | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/readonly_reentrancy.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/readonly_reentrancy_test.sol)                                                        | 0                                                                                                                |
| [NFT Approve Warning](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/nft_approve_warning.py)                              | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/nft_approve_warning.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/nft_approve_warning_test.sol)                                                        | 0                                                                                                                |
| [Multiple Storage Read](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/multiple_storage_read.py)                          | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/multiple_storage_read.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/multiple_storage_read_test.sol)                                                      | 9                                                                                                                |
| [Magic Number](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/magic_number.py)                                            | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/magic_number.md)                          | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/magic_number_test.sol)                                                               | 3                                                                                                                |
| [Inconsistent Non-Reentrant](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/inconsistent_nonreentrant.py)                 | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/inconsistent_nonreentrant.md)             | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/inconsistent_nonreentrant_test.sol)                                                  | 0                                                                                                                |
| [Falsy Only EOA Modifier](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/falsy_only_eoa_modifier.py)                      | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/falsy_only_eoa_modifier.md)               | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/falsy_only_eoa_modifier_test.sol)                                                    | 0                                                                                                                |
| [Missing Event Setter](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/event_setter.py)                                    | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/event_setter.md)                          | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/event_setter_test.sol)                                                               | 1                                                                                                                |
| [Dubious Typecast](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/dubious_typecast.py)                                    | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/dubious_typecast.md)                      | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/dubious_typecast_test.sol)                                                           | 0                                                                                                                |
| [Double Entry Token Possibility](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/double_entry_token_possibility.py)        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/double_entry_token_possibility.md)        | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/double_entry_token.sol)                                                                                                                                              | 0                                                                                                                |
| [Call Forward To Protected](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/call_forward_to_protected.py)                  | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/call_forward_to_protected.md)             | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/call_forward_to_protected_test.sol)                                                  | 0                                                                                                                |
| [Before Token Transfer](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/before_token_transfer.py)                          | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/before_token_transfer.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/before_token_transfer_test.sol)                                                      | 2                                                                                                                |
| [For Continue Increment](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/for_continue_increment.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/for_continue_increment.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/for_continue_increment.sol)                                                         | 0                                                                                                                |
| [AAVE Flasloan Callback](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/aave/flashloan_callback.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/aave/flashloan_callback.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/AaveFlashloanCallback.sol)                                                         | 0                                                                                                                |
| [Arbitrary Call](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/arbitrary_call/arbitrary_call.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/arbitrary_call.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/arbitrary_call_test.sol)                                                         | 0                                                                                                                |
| [Elliptic Curve Recover](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/ecrecover.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/ecrecover.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/ecrecover.sol)                                                         | 0                                                                                                                |
| [Public vs External](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/public_vs_external.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/public_vs_external.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/public_vs_external_test.sol)                                                         | 0                                                                                                                |
| [Balancer Read-only Reentrancy](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/balancer/balancer_readonly_reentrancy.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/balancer/readonly_reentrancy.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/balancer/readonly_reentrancy_test.sol)                                                         | 0                                                                                                                |

**Please note:**

- *Valid - issues included in reports and fixed by developers (January 2023 - June 2023).

- There are two detectors which have several checks inside: [pess-uni-v2](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/uni_v2.py) and [arbitrary-call](https://github.com/pessimistic-io/slitherin/blob/master/slitherin/detectors/arbitrary_call/arbitrary_call.py).

## Enhancements & New Detectors

Here we indicate our updates, workflows and mark completed tasks and improvements! 

> You can add your own *detector/idea/enhancement* by [opening the Issue at the following link](https://github.com/pessimistic-io/slitherin/issues).

Prior to adding a custom *detector*, ensure that:

1. In a documentation file, your detector is comprehensively described;
2. The detector test contract is presented and correctly compiles;
3. The detector code is presented and works properly.

Prior to adding an *idea*, ensure that:
1. Your concept or idea is well articulated;
2. A vulnerability example (or PoC) is provided;

Prior to adding an *enhancement*, ensure that:
1. Your enhancement does **not** make the base code worse;
2. Your enhancement is commented.

#### **Detectors Backlog:**

[![Issues](https://img.shields.io/github/issues-raw/pessimistic-io/slitherin?style=flat-square)](https://github.com/pessimistic-io/slitherin/issues)
[![Open Pool Requests](https://img.shields.io/github/issues-pr/pessimistic-io/slitherin)](https://github.com/pessimistic-io/slitherin/pulls)
[![Closed Pool Requests](https://img.shields.io/github/issues-pr-closed-raw/pessimistic-io/slitherin?style=flat-square)](https://github.com/pessimistic-io/slitherin/pulls?q=is%3Apr+is%3Aclosed)

## Acknowledgements

Our team would like to express our deepest gratitude to the [Slither tool](https://github.com/crytic/slither) creators: [Josselin Feist, Gustavo Grieco, and Alex Groce](https://arxiv.org/pdf/1908.09878.pdf), as well as [Crytic](https://github.com/crytic), [Trail of Bits'](https://blog.trailofbits.com) blockchain security division, and all the people who believe in the original tool and its evolution!

**Slitherin in mass media**

- [Week in Ethereum News](https://weekinethereumnews.com/#:~:text=Slitherin%3A%20custom%20Slither%20detectors%20with%20higher%20sensitivity%20but%20higher%20false%20positives)
- [Blockthreat](https://newsletter.blockthreat.io/p/blockthreat-week-16-2023#:~:text=Slitherin%20a%20collection%20of%20Slither%20detection%20by%20Pessimistic.io%20team)
- [Release article by officercia.eth](https://officercia.mirror.xyz/ucWYWnhBXmkKq54BIdJcH5GnrAB-nQkUsZ2F-ytEsR4)
- [Arbitrary Calls & New Slitherin Detector Release](https://blog.pessimistic.io/arbitrary-calls-new-slitherin-detector-release-f58751e61bb)
- [What’s up Slitherin?](https://blog.pessimistic.io/whats-up-slitherin-e44ea2c10618)
- [Defillama](https://t.me/defillama_tg/842)
- [Essential Tools for Auditing Smart Contracts by Hexens](https://hexens.io/blog/toolkit-for-web3-security-engineers)
- [ETH Belgrade](https://www.youtube.com/watch?v=CU9JAqGY5h8&t=3s) talk
- Integrated into [AuditWizard](https://app.auditwizard.io/)

## Thank you!

#### It would be fantastic if you could bookmark, share, star, or fork this repository. Any attention will help us achieve our common goal of making **Web3 a little bit safer** than it was before: therefore, we require your support!

[![Watch](https://img.shields.io/github/watchers/pessimistic-io/slitherin)](https://github.com/pessimistic-io/slitherin/watchers)
[![Like](https://img.shields.io/github/stars/pessimistic-io/slitherin)](https://github.com/pessimistic-io/slitherin/stargazers)
[![Fork](https://img.shields.io/github/forks/pessimistic-io/slitherin)](https://github.com/pessimistic-io/slitherin/stargazers)

#### For our part, we'll do everything in our power to ensure that this project continues to grow successfully in terms of both code and technology as well as community and professional interaction! We sincerely hope you find our work useful and appreciate any feedback, so please do not hesitate to [contact us](mailto:gm@pessimistic.io)!

[![Mail](https://img.shields.io/badge/Mail-gm%40pessimistic.io-orange?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](mailto:gm@pessimistic.io)

---
> Pessimistic delivers trusted security audits since 2017.
\
> Require expert oversight of your safety?
\
> Explore our services at [pessimistic.io](https://pessimistic.io/).

#
