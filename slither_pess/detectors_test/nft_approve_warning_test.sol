pragma solidity ^0.8.0;

contract nft_approve_warning_test {
    function transferFromOk(
        msg.sender,
        Lib.NFT calldata nft1,
        address u2,
        Lib.NFT calldata nft2
    ) public {}

    function transferFromWrong(
        address u1,
        Lib.NFT calldata nft1,
        address u2,
        Lib.NFT calldata nft2
    ) public {}
}
