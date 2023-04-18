# Pessimistic plugin for slither

**Welcome!** We are the [pessimistic.io](https://pessimistic.io/) team, and in recent months we have been actively developing our [own **Slither detectors**](https://github.com/pessimistic-io/custom_detectors/tree/master/slither_pess/detectors) to help with code review and audit process. This repository contains everything you may require to work with them: they are **fully operational and we have made them available to the public for the first time!**

The detectors are quite simple and **are not written in the "original style"**. As a result, they produce FPs (False Positives) slightly more frequently than original ones, **which is actually their primary feature**. So that, our detectors are a kind of automation of the checks implemented in the checklist, their main purpose is to look for issues and assist the code auditor.

We would also be delighted if you, dear community, let us know if you have discovered an issue via our detectors. You may contact us via opening a [PR/Issue](https://github.com/pessimistic-io/custom_detectors/issues) or [directly](mailto:gm@pessimistic.io), whichever is more convenient for you!

## Repository Navigation

#### **Table of Contents:**

| Section                      | Link                                                                                                          |
|------------------------------|---------------------------------------------------------------------------------------------------------------|
| Docs                         | [Docs for each detector](https://github.com/pessimistic-io/custom_detectors/tree/master/docs)                 |
| Slither_pess                 | [Detectors](https://github.com/pessimistic-io/custom_detectors/tree/master/slither_pess)                      |
| Tests                        | [Test contracts for detectors](https://github.com/pessimistic-io/custom_detectors/tree/master/tests)          |
| Utils                        | [Auxiliary files](https://github.com/pessimistic-io/custom_detectors/tree/master/utils)                       |
| Issues                       | [Suggest an idea](https://github.com/pessimistic-io/custom_detectors/issues)                                  |
| Installation Process         | [Step-by-Step guide](https://github.com/pessimistic-io/custom_detectors#installation-process)                 |
| Development & Customization  | [Tips for developers](https://github.com/pessimistic-io/custom_detectors#development--customization)          |
| Enhancements & New Detectors | [Project's Improvements](https://github.com/pessimistic-io/custom_detectors#enhancements--new-detectors)      |
| BackLog                      | [Explore Backlog](https://github.com/pessimistic-io/custom_detectors/blob/master/README.md#detectors-backlog) |

#### **Detectors & Docs:**

| Detector Link                                                                                                                                             | Docs & Setup                                                                                                     |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| [Unprotected Setter](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/unprotected_setter.py)                         | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/unprotected_setter.md)             |
| [Unprotected Initialize](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/unprotected_initialize.py)                 | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/unprotected_initialize.md)         |
| [TX Gasprice Warning](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/tx_gasprice_warning.py)                       | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/tx_gasprice_warning.md)            |
| [UniswapV2 Integration](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/uni_v2.py)                                  | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/integration_uniswapV2.md)          |
| [Token Fallback](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/token_fallback.py)                                 | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/token_fallback.md)                 |
| [Timelock Controller](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/timelock_controller.py)                       | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/timelock_controller.md)            |
| [Strange Setter](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/strange_setter.py)                                 | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/strange_setter.md)                 |
| [Read-only Reentrancy](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/read_only_reentrancy.py)                     | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/readonly_reentrancy.md)            |
| [NFT Approve Warning](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/nft_approve_warning.py)                       | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/nft_approve_warning.md)            |
| [Multiple Storage Read](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/multiple_storage_read.py)                   | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/multiple_storage_read.md)          |
| [Magic Number](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/magic_number.py)                                     | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/magic_number.md)                   |
| [Inconsistent Non-Reentrant](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/inconsistent_nonreentrant.py)          | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/inconsistent_nonreentrant.md)      |
| [Falsy Only EOA Modifier](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/falsy_only_eoa_modifier.py)               | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/falsy_only_eoa_modifier.md)        |
| [Missing Event Setter](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/event_setter.py)                             | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/event_setter.md)                   |
| [Dubious Typecast](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/dubious_typecast.py)                             | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/dubious_typecast.md)               |
| [Double Entry Token Possibility](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/double_entry_token_possibility.py) | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/double_entry_token_possibility.md) |
| [Call Forward To Protected](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/call_forward_to_protected.py)           | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/call_forward_to_protected.md)      |
| [Before Token Transfer](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/before_token_transfer.py)                   | [Explore](https://github.com/pessimistic-io/custom_detectors/blob/master/docs/before_token_transfer.md)          |

## Installation Process

To add and use our detectors, you must first install a special plugin, the functionality of which is described in the [original ToB's Slither repository](https://github.com/crytic/slither). We strongly recommend that you read it at [the following link](https://github.com/crytic/slither) for a deeper understanding of the principles of our detectors!

To install the detectors properly, simply copy the original Slither repository, then clone our repository, and after that run a single command (listed in below). **Keep in mind that in order to test the detectors on test contracts, dependencies must be installed!**

> Please note: there is one detector that is disabled by default: [pess-uni-v2](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/uni_v2.py). **It is recommended to run it only on projects that integrate UniswapV2!**

With Slither installed, run the following command in the repository folder:

```bash
python3 setup.py develop

```

## Development & Customization

1. Making changes in the detector code;
2. Run `slither` on the test file, specifying through the `--detect` flag the name of the detector.

> Keep in mind that you don't have to reinstall the plugin every time you use it!

- Check out the [documentation](https://github.com/trailofbits/slither/wiki/Adding-a-new-detector) here.
- We would also like to invite you to [visit our blog](https://blog.pessimistic.io/) and [read our article about the Slither](https://blog.pessimistic.io/slither-an-auditors-cornucopia-a8793ea96e67)! 

## Enhancements & New Detectors

Here we indicate our updates, workflows and mark completed tasks and improvements. You can add your idea for improvement by [opening the Issue at the following link](https://github.com/pessimistic-io/custom_detectors/issues)! 

> We also have some "tasty" statistics data on current detector alarms, which we have been collecting since January 2022. These alarms are also included in our reports that we send to our customers. You can check it out at the following link: [GoogleDoc Link](https://docs.google.com/spreadsheets/d/1koDJ5y5oYYUP35Jm7jXE_VzW1XzDkrWbfX2sa6KLgx0/edit?hl=ru#gid=0)

#### **Detectors Backlog:**

| Task                                                                                                                                  | Status     |
|---------------------------------------------------------------------------------------------------------------------------------------|------------|
| Update No.1                                                                                                                           | In Process |
| Fix - Reentrancy Detector                                                                                                             | Completed  |
| Suggestion - Write a Walkthrough Article                                                                                              | In Process |
| Add [UniswapV2 Integration](https://github.com/pessimistic-io/custom_detectors/blob/master/slither_pess/detectors/uni_v2.py) Detector | Completed  |

#

**We hope you find our work useful; we would appreciate any feedback, so please do not hesitate to [contact us](mailto:gm@pessimistic.io)!**
