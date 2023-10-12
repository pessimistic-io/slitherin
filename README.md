#  Slitherin by Pessimistic.io

[![Blog](https://img.shields.io/badge/Blog-Link-blue?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](https://blog.pessimistic.io/)
[![Our Website](https://img.shields.io/badge/By-pessimistic.io-green?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](https://pessimistic.io/)
[![Mail](https://img.shields.io/badge/Mail-gm%40pessimistic.io-orange?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](mailto:gm@pessimistic.io)

**Welcome!** We are the [pessimistic.io](https://pessimistic.io/) team, and in recent months we have been actively developing our [own **Slither detectors**](https://github.com/pessimistic-io/slitherin/tree/master/slither_pess/detectors) to help with code review and audit process. This repository contains everything you may require to work with them!

We increased the sensitivity of our detectors since they are *quite straightforward* and not written in the "original style." As a result, they produce FPs ([False Positives](https://en.wikipedia.org/wiki/False_positives_and_false_negatives)) more frequently than original ones. So that, our detectors are a kind of automation of the checks implemented in the checklist, their main purpose is to look for issues and assist the code auditor.

Please let us know if you have discovered an [issue/bug/vulnerability](https://telegra.ph/BountyCTF-Platforms-Web3-04-19) via our custom Slither detectors. You may contact us via opening a [PR/Issue](https://github.com/pessimistic-io/slitherin/issues) or [directly](mailto:gm@pessimistic.io), whichever is more convenient for you. If you have any further questions or suggestions, please [join our Discord Server](https://discord.gg/vPxkR8B9p7) or [Telegram chat](https://t.me/+G96ejJ7Pmgk1NDZi)! We hope to see you there, and we intend to support the community and its initiatives!

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/+t8dRfLLbVx1iYzNi)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/vPxkR8B9p7)

## Repository Navigation

#### **Table of Contents:**

| Section                      | Link                                                                                                          |
|------------------------------|---------------------------------------------------------------------------------------------------------------|
| Docs                         | [Docs for each detector](https://github.com/pessimistic-io/slitherin/tree/master/docs)                        |
| Slither_pess                 | [Detectors code](https://github.com/pessimistic-io/slitherin/tree/master/slither_pess)                        |
| Tests                        | [Test contracts for detectors](https://github.com/pessimistic-io/slitherin/tree/master/tests)                 |
| Utils                        | [Auxiliary files](https://github.com/pessimistic-io/slitherin/tree/master/utils)                              |
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
4. Run the original Slither as usual.
5. Dependencies must be installed in order to test the detectors on our test contracts:
```bash
npm install
```
### Using Pip
1. Install the [original Slither](https://github.com/crytic/slither#how-to-install);
2. Install the pip [package](https://pypi.org/project/slitherin/):
```bash
pip install slitherin
```
3. Run the original Slither as usual.

## **Detectors Table**

| Detector Link                                                                                                                                             | Docs & Setup                                                                                                     | Test Contract                                                                                                                                             | Valid* Issues                                                                                                    |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| [Unprotected Setter](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/unprotected_setter.py)                                | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/unprotected_setter.md)                    | In progress                                                                                                                                               | 1                                                                                                                |
| [Unprotected Initialize](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/unprotected_initialize.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/unprotected_initialize.md)                | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/unprotected_initialize_test.sol)                                                     | 0                                                                                                                |
| [TX Gasprice Warning](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/tx_gasprice_warning.py)                              | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/tx_gasprice_warning.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/tx_gasprice_warning_test.sol)                                                        | 0                                                                                                                |
| [UniswapV2 Integration](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/uni_v2.py)                                         | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/integration_uniswapV2.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/Bad_UniswapV2_test.sol)                                                              | 0                                                                                                                |
| [Token Fallback](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/token_fallback.py)                                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/token_fallback.md)                        | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/token_fallback_test.sol)                                                             | 0                                                                                                                |
| [Timelock Controller](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/timelock_controller.py)                              | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/timelock_controller.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/timelock_controller_test.sol)                                                        | 1                                                                                                                |
| [Strange Setter](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/strange_setter.py)                                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/strange_setter.md)                        | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/strange_setter_test.sol)                                                             | 0                                                                                                                |
| [Read-only Reentrancy](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/read_only_reentrancy.py)                            | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/readonly_reentrancy.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/readonly_reentrancy_test.sol)                                                        | 0                                                                                                                |
| [NFT Approve Warning](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/nft_approve_warning.py)                              | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/nft_approve_warning.md)                   | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/nft_approve_warning_test.sol)                                                        | 0                                                                                                                |
| [Multiple Storage Read](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/multiple_storage_read.py)                          | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/multiple_storage_read.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/multiple_storage_read_test.sol)                                                      | 9                                                                                                                |
| [Magic Number](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/magic_number.py)                                            | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/magic_number.md)                          | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/magic_number_test.sol)                                                               | 3                                                                                                                |
| [Inconsistent Non-Reentrant](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/inconsistent_nonreentrant.py)                 | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/inconsistent_nonreentrant.md)             | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/inconsistent_nonreentrant_test.sol)                                                  | 0                                                                                                                |
| [Falsy Only EOA Modifier](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/falsy_only_eoa_modifier.py)                      | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/falsy_only_eoa_modifier.md)               | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/falsy_only_eoa_modifier_test.sol)                                                    | 0                                                                                                                |
| [Missing Event Setter](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/event_setter.py)                                    | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/event_setter.md)                          | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/event_setter_test.sol)                                                               | 1                                                                                                                |
| [Dubious Typecast](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/dubious_typecast.py)                                    | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/dubious_typecast.md)                      | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/dubious_typecast_test.sol)                                                           | 0                                                                                                                |
| [Double Entry Token Possibility](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/double_entry_token_possibility.py)        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/double_entry_token_possibility.md)        | In progress                                                                                                                                               | 0                                                                                                                |
| [Call Forward To Protected](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/call_forward_to_protected.py)                  | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/call_forward_to_protected.md)             | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/call_forward_to_protected_test.sol)                                                  | 0                                                                                                                |
| [Before Token Transfer](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/before_token_transfer.py)                          | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/before_token_transfer.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/before_token_transfer_test.sol)                                                      | 2                                                                                                                |
| [For Continue Increment](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/for_continue_increment.py)                        | [Explore](https://github.com/pessimistic-io/slitherin/blob/master/docs/for_continue_increment.md)                 | [Test](https://github.com/pessimistic-io/slitherin/blob/master/tests/for_continue_increment.sol)                                                         | 0                                                                                                                |

**Please note:**

- *Valid - issues included in reports and fixed by developers (January 2023 - June 2023).

- There is one integration detector which has several checks inside: [pess-uni-v2](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/uni_v2.py). **It runs only on projects that integrate [Uniswap V2](https://betterprogramming.pub/uniswap-v2-in-depth-98075c826254)!**

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

| Task                                                                                                                                  | Status     |
|---------------------------------------------------------------------------------------------------------------------------------------|------------|
| Opensource current repository                                                                                                         | Completed  |
| Fix - Readonly Reentrancy Detector                                                                                                    | Completed  |
| Suggestion - Write a Walkthrough Article                                                                                              | Completed  |
| Add [UniswapV2 Integration](https://github.com/pessimistic-io/slitherin/blob/master/slither_pess/detectors/uni_v2.py) detector        | Completed  |
| For-continue-increment - add detector                                                                                                 | Completed  |
| Refactor python code. Make it cleaner.                                                                                                | TODO       |
| Nft-approve-warning detector - remove detection with "this" as a first parameter in "transferFrom()" function                         | TODO       |
| Strange-setter detector - remove detection when mappings or structs are set                                                           | TODO       |
| Double-entry-token detector - remove detection of ETH transfers                                                                       | TODO       |
| Before-token-transfer detector - remove detection with "virtual" modifier and "super" function call                                   | TODO       |
| Strange-constructor detector - remove detection of constructor function with base constructor                                         | TODO       |

## Acknowledgements

Our team would like to express our deepest gratitude to the [Slither tool](https://github.com/crytic/slither#how-to-install) creators: [Josselin Feist, Gustavo Grieco, and Alex Groce](https://arxiv.org/pdf/1908.09878.pdf), as well as [Crytic](https://github.com/crytic), [Trail of Bits'](https://blog.trailofbits.com) blockchain security division, and all the people who believe in the original tool and its evolution!

**Articles:**

- [Slither](https://github.com/crytic/slither#how-to-install)
- [How do we use Slither at Pessimistic.io](https://blog.pessimistic.io/slither-an-auditors-cornucopia-a8793ea96e67)
- [Slither Explained](https://telegra.ph/Slither-Explained-04-19)
- [Slither: In-Depth](https://medium.com/coinmonks/slither-smart-contract-security-tools-29918df0fa8c)
- [Slither Review](https://blog.trailofbits.com/2019/05/27/slither-the-leading-static-analyzer-for-smart-contracts/)
- [Slither - Python](https://pypi.org/project/slither-analyzer/)
- [Reentrancy Attacks on Smart Contracts Distilled](https://blog.pessimistic.io/reentrancy-attacks-on-smart-contracts-distilled-7fed3b04f4b6)
- Be sure to [check out our blog](https://blog.pessimistic.io/) as well!

**Research Papers:**

- [Slither: A Static Analysis Framework For Smart Contracts](https://arxiv.org/pdf/1908.09878.pdf)
- [Detecting Vulnerable Ethereum Smart Contracts via Abstracted Vulnerability Signatures](https://arxiv.org/pdf/1912.04466.pdf)
- [Evaluating Smart Contract Static Analysis Tools Using Bug Injection](https://arxiv.org/pdf/2005.11613.pdf)
- [A Framework and DataSet for Bugs in Ethereum Smart Contracts](https://arxiv.org/pdf/2009.02066.pdf)
- [A Comprehensive Survey of Upgradeable Smart Contract Patterns](https://arxiv.org/pdf/2304.03405.pdf)

**Slither: In-Depth**

- [Accessing Private Data in Smart contracts](https://quillaudits.medium.com/accessing-private-data-in-smart-contracts-quillaudits-fe847581ce6d)
- [Simplest way to run Slither for your Smart Contract project](https://coinsbench.com/simplest-way-to-run-slither-for-your-smart-contract-project-4bdb367c06e2)
- [Slither Notes](https://hackmd.io/@DRViPNz-TVC6wqdRF8LP6w/HJHcycB9t)
- [Dataset Card for Slither Audited Smart Contracts](https://huggingface.co/datasets/mwritescode/slither-audited-smart-contracts)
- [Auditing Tools Report: Slither](https://hackmd.io/@Ydcnh_SKTIqqOYzr7HhBvQ/B1X7o1dij)
- [Bridge Security Checklist: Client Side](https://hackmd.io/@cbym/HJWQglwNs)
- [Slither & Echidna + Remappings](https://www.justinsilver.com/technology/programming/slither-echidna-remappings/)
- [Static Analysis of Smart Contracts with Slither & GitHub Actions](https://medium.com/coinmonks/static-analysis-of-smart-contracts-with-slither-github-actions-1e67e54ed8a7)

**Slitherin in mass media**

- [Week in Ethereum News](https://weekinethereumnews.com/#:~:text=Slitherin%3A%20custom%20Slither%20detectors%20with%20higher%20sensitivity%20but%20higher%20false%20positives)
- [Blockthreat](https://newsletter.blockthreat.io/p/blockthreat-week-16-2023#:~:text=Slitherin%20a%20collection%20of%20Slither%20detection%20by%20Pessimistic.io%20team)
- [Release article by officercia.eth](https://officercia.mirror.xyz/ucWYWnhBXmkKq54BIdJcH5GnrAB-nQkUsZ2F-ytEsR4)
- [Defillama](https://t.me/defillama_tg/842)
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
