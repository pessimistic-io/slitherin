# NFT Approve Warning

## Configuration
* Check: `nft-approve-warning`
* Severity: `Medium`
* Confidence: `High`

## Description
Sees if contract contains `erc721.[safe]TransferFrom(from, ...)` where from parameter is not related to msg.sender.
An attacker can steal any approved NFTs because `transferFrom` function does NOT check that the call is made by its' owner. 

## Exploit Scenario
[Exploit](../tests/nft_approve_warning_test.sol) 

## Related attack
https://ventral.digital/posts/2022/8/18/sznsdaos-bountyboard-unauthorized-transferfrom-vulnerability

## Recommendation
Make sure that in `erc721.[safe]TransferFrom(from, ...)` functions `from` parameter is related to `msg.sender`.