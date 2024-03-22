// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;
contract Test {
    function vulnerableArbPrevrandao() external view returns (uint256 prevRandao) {
        prevRandao = block.prevrandao;
    }

    function vulnerableArbDifficulty() external view returns (uint256 difficulty) {
        difficulty = block.difficulty;
    }

    function vulnerableArbPrevrandaoAndDifficulty() external view returns (uint256 prevRandao, uint256 difficulty) {
        prevRandao = block.prevrandao;
        difficulty = block.difficulty;
    }

    function vulnerableArbPrevrandaoYul() external view returns (uint256 prevRandao) {
        assembly {
            prevRandao := prevrandao()
        }
    }

    function vulnerableAllWithYul() external view returns (uint256 prevRandao1, uint256 diff1, uint256 prevRandao2) {
        prevRandao1 = block.prevrandao;
        diff1 = block.difficulty;
        assembly {
            prevRandao2 := prevrandao()
        }
    }
}