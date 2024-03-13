# NFT Approve Warning

## Configuration
* Check: `pess-nft-approve-warning`
* Severity: `Medium`
* Confidence: `Low`

## Description
The detector sees if a contract contains `erc721.[safe]TransferFrom(from, ...)` or `erc1155.safe[Batch]TransferFrom(from, ...)` where `from` parameter is not related to `msg.sender`.
An attacker can steal any approved NFTs because `transferFrom` function does NOT check that the call is made by its owner. 

## Vulnerable Scenario
[test scenario](../tests/nft_approve_warning_test.sol) 

## Related attack

[Unauthorized transfer_from Vulnerability](https://ventral.digital/posts/2022/8/18/sznsdaos-bountyboard-unauthorized-transferfrom-vulnerability)

## Recommendation
Make sure that in `erc721.[safe]TransferFrom(from, ...)` and `erc1155.safe[Batch]TransferFrom(from, ...)` functions `from` parameter is related to `msg.sender`.
