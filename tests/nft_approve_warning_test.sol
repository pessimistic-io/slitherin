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

pragma solidity ^0.8.19;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

contract Test
{
    IERC20 immutable TOKEN = IERC20(address(0));
    function test() internal {
        TOKEN.transferFrom(address(this), address(0), 0);
    }
}

