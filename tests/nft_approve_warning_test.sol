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

interface IERC1155 {
    function safeTransferFrom(address from, address to, uint256 id, uint256 value, bytes memory data) external;
    function safeBatchTransferFrom(
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory values,
        bytes memory data
    ) external;
}

contract TestERC1155 {
    function vuln_safeTransferFrom(address target, address from, address to) external {
        IERC1155(target).safeTransferFrom(from, to, 1, 1, "");
    }

    function ok_safeTransferFrom(address target, address to) external {
        IERC1155(target).safeTransferFrom(msg.sender, to, 1, 1, "");
    }

    function vuln_safeBatchTransferFrom(address target, address from, address to) external {
        IERC1155(target).safeBatchTransferFrom(from, to, new uint256[](2), new uint256[](2), "");
    }

    function ok_safeBatchTransferFrom(address target, address to) external {
        IERC1155(target).safeBatchTransferFrom(msg.sender, to, new uint256[](2), new uint256[](2), "");
    }
}


library SafeERC20 {
    function safeTransferFrom(IERC20 token, address from, address to, uint256 value) internal {
        // _callOptionalReturn(token, abi.encodeCall(token.transferFrom, (from, to, value)));
    }
}

contract TestSafeERC20LibCall {
    function vuln1_safeErc20TransferFrom(IERC20 token, address from, address to, uint256 value) external {
        SafeERC20.safeTransferFrom(token, from, to, value);
    }

    function ok1_safeErc20TransferFrom(IERC20 token, address to, uint256 value) external {
        SafeERC20.safeTransferFrom(token, msg.sender, to, value);
    }

    function vuln2_safeErc20TransferFrom(address from, address to, uint256 value) external {
        SafeERC20.safeTransferFrom(IERC20(msg.sender), from, to, value);
    }

    function ok2_safeErc20TransferFrom(address to, uint256 value) external {
        SafeERC20.safeTransferFrom(IERC20(msg.sender), msg.sender, to, value);
    }
}
