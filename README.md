#  Slither Detectors by Pessimistic.io

[![Blog](https://img.shields.io/badge/Blog-Link-blue?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](https://blog.pessimistic.io/)
[![Our Website](https://img.shields.io/badge/By-pessimistic.io-green?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](https://pessimistic.io/) 
[![Mail](https://img.shields.io/badge/Mail-gm%40pessimistic.io-orange?style=flat-square&logo=appveyor?logo=data:https://pessimistic.io/favicon.ico)](mailto:gm@pessimistic.io)

**Welcome!** We are the [pessimistic.io](https://pessimistic.io/) team, and in recent months we have been actively developing our [own **Slither detectors**](https://github.com/pessimistic-io/custom_detectors/tree/master/slither_pess/detectors) to help with code review and audit process. This repository contains everything you may require to work with them!

We increased the sensitivity of our detectors since they are *quite straightforward* and not written in the "original style." As a result, they produce FPs ([False Positives](https://en.wikipedia.org/wiki/False_positives_and_false_negatives)) more frequently than original ones. So that, our detectors are a kind of automation of the checks implemented in the checklist, their main purpose is to look for issues and assist the code auditor.

Please let us know if you have discovered an [issue/bug/vulnerability](https://telegra.ph/BountyCTF-Platforms-Web3-04-19) via our custom Slither detectors. You may contact us via opening a [PR/Issue](https://github.com/pessimistic-io/custom_detectors/issues) or [directly](mailto:gm@pessimistic.io), whichever is more convenient for you. If you have any further questions or suggestions, please [join our Discord Server](https://discord.gg/vPxkR8B9p7)! We hope to see you there, and we intend to support the community and its initiatives!

## Repository Navigation

#### **Table of Contents:**

| Section                      | Link                                                                                                          |
|------------------------------|---------------------------------------------------------------------------------------------------------------|
| Docs                         | [Docs for each detector](https://github.com/pessimistic-io/custom_detectors/tree/master/docs)                 |
| Slither_pess                 | [Detectors code](https://github.com/pessimistic-io/custom_detectors/tree/master/slither_pess)                 |
| Tests                        | [Test contracts for detectors](https://github.com/pessimistic-io/custom_detectors/tree/master/tests)          |
| Utils                        | [Auxiliary files](https://github.com/pessimistic-io/custom_detectors/tree/master/utils)                       |
| Issues                       | [Suggest an idea](https://github.com/pessimistic-io/custom_detectors/issues)                                  |
| Installation Process         | [Step-by-Step guide](https://github.com/pessimistic-io/custom_detectors#installation-process)                 |
| Detectors                    | [Detectors table](https://github.com/pessimistic-io/custom_detectors#detectors-table)                         |
| Enhancements & New Detectors | [Project Improvements](https://github.com/pessimistic-io/custom_detectors#enhancements--new-detectors)        |

## Installation Process

To install Pessimistic Detectors: 
1. Install the [original Slither](https://github.com/crytic/slither#how-to-install);
2. Clone our repository;
3. Run the following command in our repository folder:
```bash
python3 setup.py develop
```
> Keep in mind that you don't have to reinstall the plugin after changes in the repository!
4. Dependencies must be installed in order to test the detectors on our test contracts:
```bash
npm install
```

## **Detectors Table**

> Follow [contribution guidelines](https://telegra.ph/Table-MD-Contribution-Guidelines-04-20) if you want to add your own data or links into our table!

| Section                      | Link                                                                                                          | Test Contract | Valid* Issue |
|------------------------------|---------------------------------------------------------------------------------------------------------------|---------------|--------------|
| Docs                         | [Docs for each detector](https://github.com/pessimistic-io/custom_detectors/tree/master/docs)                 |               |              |
| Slither_pess                 | [Detectors](https://github.com/pessimistic-io/custom_detectors/tree/master/slither_pess)                      |               |              |
| Tests                        | [Test contracts for detectors](https://github.com/pessimistic-io/custom_detectors/tree/master/tests)          |               |              |
| Utils                        | [Auxiliary files](https://github.com/pessimistic-io/custom_detectors/tree/master/utils)                       |               |              |
| Issues                       | [Suggest an idea](https://github.com/pessimistic-io/custom_detectors/issues)                                  |               |              |
| Installation Process         | [Step-by-Step guide](https://github.com/pessimistic-io/custom_detectors#installation-process)                 |               |              |
| Development & Customization  | [Tips for developers](https://github.com/pessimistic-io/custom_detectors#development--customization)          |               |              |
| Enhancements & New Detectors | [Project's Improvements](https://github.com/pessimistic-io/custom_detectors#enhancements--new-detectors)      |               |              |
| BackLog                      | [Explore Backlog](https://github.com/pessimistic-io/custom_detectors/blob/master/README.md#detectors-backlog) |               |              |

**Please note:**

- *Valid - issues included in reports and fixed by developers!

- There is one detector that is disabled by default: [pess-uni-v2](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/uni_v2.py). **It is recommended to run it only on projects that integrate [Uniswap V2](https://betterprogramming.pub/uniswap-v2-in-depth-98075c826254)!**

## Enhancements & New Detectors

Here we indicate our updates, workflows and mark completed tasks and improvements! 

> You can add your own *detector/idea/enhancement* by [opening the Issue at the following link](https://github.com/pessimistic-io/custom_detectors/issues).

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

[![Issues](https://img.shields.io/github/issues/pessimistic-io/custom_detectors?style=flat-square)](https://github.com/pessimistic-io/custom_detectors/issues)
[![Open Pool Requests](https://img.shields.io/github/issues-pr/pessimistic-io/custom_detectors?style=flat-square)](https://github.com/pessimistic-io/custom_detectors/pulls)
[![Closed Pool Requests](https://img.shields.io/github/issues-pr-closed-raw/pessimistic-io/custom_detectors?style=flat-square)](https://github.com/pessimistic-io/custom_detectors/pulls?q=is%3Apr+is%3Aclosed)

| Task                                                                                                                                  | Status     |
|---------------------------------------------------------------------------------------------------------------------------------------|------------|
| Opensource current repository                                                                                                         | In Process |
| Fix - Readonly Reentrancy Detector                                                                                                    | Completed  |
| Suggestion - Write a Walkthrough Article                                                                                              | In Process |
| Add [UniswapV2 Integration](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/uni_v2.py) Detector | Completed  |

## Articles:

- [How do we use Slither at Pessimistic.io](https://blog.pessimistic.io/slither-an-auditors-cornucopia-a8793ea96e67)
- [Slither: In-Depth](https://medium.com/coinmonks/slither-smart-contract-security-tools-29918df0fa8c)
- [Slither Review](https://blog.trailofbits.com/2019/05/27/slither-the-leading-static-analyzer-for-smart-contracts/)

#

### We would also like to invite you to [visit our blog](https://blog.pessimistic.io/)!
### **We hope you find our work useful; we would appreciate any feedback, so please do not hesitate to [contact us](mailto:gm@pessimistic.io)!**
