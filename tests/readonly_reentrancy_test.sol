//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

// Definition for read-only reentrancy:
// There is a read-only function that returns a value which is affected
// by the state of the contract that was modified after potential reentrant call.
import "./interfaces/IERC721.sol";

contract MinimalReeentrant {
    uint256 private _number;

    function vulnarableGetter() public view returns (uint256) {
        return _number;
    }

    function reentrancyExploitable() public {
        msg.sender.call("");
        _number++;
    }
}

contract MinimalVictim {
    address public reentrant;

    function doSmth() public {
        MinimalReeentrant reentrant = MinimalReeentrant(reentrant);
        uint256 x = reentrant.vulnarableGetter() + 1;
    }
}

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
    function vulnarableVictimGetter(
        address reentrant
    ) public view returns (uint256) {
        return Reeentrant(reentrant).vulnarableGetter();
    }

    function vulnarableVictimGetter2(
        address reentrant
    ) public view returns (uint256) {
        return internalRead(reentrant);
    }

    function internalRead(address reentrant) internal view returns (uint256) {
        return Reeentrant(reentrant).vulnarableGetter();
    }

    modifier vulnarableVictimModifier(address reentrant) {
        _;
        require(Reeentrant(reentrant).vulnarableGetter() == 0);
    }

    function vulnarableFunction(address reentrant) public {
        Reeentrant reentrant = Reeentrant(reentrant);
        uint256 x;
        reentrant.notVulnarableGetter();
        reentrant.notVulnarableGetter2();
        reentrant.notVulnarableGetter3(1);

        reentrant.vulnarableGetter();
        x = reentrant.vulnarableGetter2();
        x = reentrant.vulnarableGetter3();
        x = reentrant.vulnarableGetter4();
        x = reentrant.vulnarableGetter5();
        reentrant.notVulnarableGetter4();
    }

    function vulnarableFunctionWithModifier(
        address reentrant
    ) public vulnarableVictimModifier(reentrant) {}

    function notVulnarableFunction(Reeentrant reentrant) public {
        uint256 x;
        x = reentrant.notVulnarableGetter();
    }
}

contract SecondaryVictim {
    uint256 private _numberS;

    function vulnarableSecondaryVictim(
        address victim,
        address reentrant
    ) public returns (uint256) {
        _numberS = Victim(victim).vulnarableVictimGetter(reentrant);
        return _numberS;
    }

    function vulnarableSecondaryVictim2(
        address victim,
        address reentrant
    ) public returns (uint256) {
        _numberS = Victim(victim).vulnarableVictimGetter2(reentrant);
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

    function vulnarableComplexVictim(
        address reentrant
    ) public returns (uint256) {
        _x = ReentrantComplex(reentrant).getVirtualPrice();
        return _x;
    }
}

contract FalsePositive {
    function notVulnarable() public {
        DummyToken(msg.sender).balanceOf(msg.sender);
    }

    uint256 balance0;
    uint256 balance1;
    uint256 managerBalance0;
    uint256 managerBalance1;
    DummyToken token0 = DummyToken(zero);
    DummyToken token1 = DummyToken(zero);
    address zero = address(0);

    function withdrawManagerBalance() external {
        uint256 amount0 = managerBalance0;
        uint256 amount1 = managerBalance1;

        managerBalance0 = 0;
        managerBalance1 = 0;

        if (amount0 > 0) {
            DummyToken(zero).transfer(zero, amount0);
        }

        if (amount1 > 0) {
            DummyToken(zero).transfer(zero, amount1);
        }
    }

    function _applyFees(uint256 _fee0, uint256 _fee1) private {
        balance0 += _fee0 / 100;
        balance1 += _fee1 / 100;
        managerBalance0 += _fee0 / 100;
        managerBalance1 += _fee1 / 100;
    }

    function _rebalance() public {
        uint256 leftover0 = token0.balanceOf(address(this)) - managerBalance0;
        uint256 leftover1 = token1.balanceOf(address(this)) - managerBalance1;
        uint256 feesEarned0 = leftover0;
        uint256 feesEarned1 = leftover1;
        _applyFees(feesEarned0, feesEarned1);
    }
}

//TODO(yhtiyar): add example with Balancer Vault read-only exlpoit (setiment hack)
