//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

// Definition for read-only reentrancy:
// There is a read-only function that returns a value which is affected
// by the state of the contract that was modified after potential reentrant call.
import "./interfaces/IERC721.sol";

contract Reeentrant {
    mapping(uint256 => uint256) private _mapping;
    uint256 private _number;
    uint256 private _number2;
    uint256 private _number_ok;

    function vulnarableGetter() public view returns (uint256) {
        return _number;
    }

    function vulnarableGetter2() public view returns (uint256) {
        return _number + 10;
    }

    function vulnarableGetter3() public view returns (uint256) {
        return vulnarableGetter();
    }

    function vulnarableGetter4() public view returns (uint256) {
        return vulnarableGetter3();
    }

    function vulnarableGetter5() public view returns (uint256) {
        return _mapping[_number];
    }

    function notVulnarableGetter() public view returns (uint256) {
        return 1;
    }

    function notVulnarableGetter2() public view returns (uint256) {
        return _mapping[1];
    }

    function notVulnarableGetter3(uint256 x) public view returns (uint256) {
        return _mapping[x];
    }

    function notVulnarableGetter4() public view returns (uint256) {
        return _number_ok;
    }

    function reentrancyExploitable() public {
        msg.sender.call("");
        _number++;
    }

    function reentrancyExploitable2() public {
        IERC721(msg.sender).safeTransferFrom(
            address(this),
            address(msg.sender),
            1
        );
        _number++;
    }

    function reentrancyExploitable3() public {
        msg.sender.call("");
        _changeState();
    }

    function reentrancyExploitable4() public {
        reentrancyExploitable3();
        _number2++;
    }

    function _changeState() internal {
        _number++;
    }

    function ok() public {
        _number_ok++;
        msg.sender.call("");
    }

    function ok2() public {
        _changeState();
        _number_ok++;
    }
}

contract Victim {
    function vulnarableVictimGetter(address reentrant)
        public
        view
        returns (uint256)
    {
        return Reeentrant(reentrant).vulnarableGetter();
    }

    modifier vulnarableVictimModifier(address reentrant) {
        _;
        require(Reeentrant(reentrant).vulnarableGetter() == 0);
    }

    function vulnarableFunction(address reentrant) public {
        Reeentrant reentrant = Reeentrant(reentrant);
        uint256 x;
        x = reentrant.vulnarableGetter();
        x = reentrant.vulnarableGetter();
        x = reentrant.vulnarableGetter2();
        x = reentrant.vulnarableGetter3();
        x = reentrant.vulnarableGetter4();
        x = reentrant.vulnarableGetter5();
        x = reentrant.notVulnarableGetter();
        x = reentrant.notVulnarableGetter2();
        x = reentrant.notVulnarableGetter3(1);
        x = reentrant.notVulnarableGetter4();
    }

    function vulnarableFunctionWithModifier(address reentrant)
        public
        vulnarableVictimModifier(reentrant)
    {}

    function notVulnarableFunction(Reeentrant reentrant) public {
        uint256 x;
        x = reentrant.notVulnarableGetter();
    }
}

contract SecondaryVictim {
    uint256 private _numberS;

    function vulnarableSecondaryVictim(address victim, address reentrant)
        public
        returns (uint256)
    {
        _numberS = Victim(victim).vulnarableVictimGetter(reentrant);
        return _numberS;
    }
}

contract DummyToken {
    mapping(address => uint256) private _balances;
    uint256 private _totalSupply;

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    function transfer(address recipient, uint256 amount) public returns (bool) {
        _balances[msg.sender] -= amount;
        _balances[recipient] += amount;
        return true;
    }

    function burn(uint256 amount) public {
        _balances[msg.sender] -= amount;
        _totalSupply -= amount;
    }
}

contract ReentrantComplex {
    address[] private _tokenAddresses;
    address private _lpTokenAddress;

    function getVirtualPrice() public view returns (uint256) {
        uint256 sum;
        for (uint256 i = 0; i < _tokenAddresses.length; i++) {
            sum += DummyToken(_tokenAddresses[i]).balanceOf(address(this));
        }
        return sum / DummyToken(_lpTokenAddress).balanceOf(address(this));
    }

    function complexReentrantExploitable() public {
        DummyToken(_lpTokenAddress).burn(1);
        msg.sender.call("");
        for (uint256 i = 0; i < _tokenAddresses.length; i++) {
            DummyToken(_tokenAddresses[i]).transfer(address(msg.sender), 100);
        }
    }
}

contract VictimForComplex {
    uint256 private _x;

    function vulnaravleComplexVictim(address reentrant)
        public
        returns (uint256)
    {
        _x = ReentrantComplex(reentrant).getVirtualPrice();
        return _x;
    }
}

contract FalsePositive {
    function notVulnarable() public {
        DummyToken(msg.sender).balanceOf(msg.sender);
    }
}
