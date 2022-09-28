//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import './interfaces/IERC721.sol';

contract nft_approve_warning_test {

    function safeTransferArt_vulnurable(address to, IERC721 nft, uint256 tokenId) external {

        nft.safeTransferFrom(nft.ownerOf(tokenId), to, tokenId);
    }

    function transferArt_vulnurable(address to, IERC721 nft, uint256 tokenId) external {

        nft.transferFrom(nft.ownerOf(tokenId), to, tokenId);
    }

    function transferArt(address to, IERC721 nft, uint256 tokenId) external {

        nft.transferFrom(msg.sender, to, tokenId);
    }

}