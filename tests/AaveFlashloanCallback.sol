contract AaveFlashloanReceiverOk {
    address POOL;

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        params;
        require(
            initiator == address(this),
            "Wallet::executeOperation: FORBIDDEN"
        );
        require(
            msg.sender == address(POOL),
            "Wallet::executeOperation: FORBIDDEN"
        );
        //doing transfer
        // for (uint i = 0; i < assets.length; i++) {
        //     uint amountOwing = amounts[i].add(premiums[i]);
        //     IERC20(assets[i]).approve(address(POOL), amountOwing);
        // }
        return true;
    }
}

contract AaveFlashloanReceiverVulnerable {
    address POOL;

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        //doing transfer
        // for (uint i = 0; i < assets.length; i++) {
        //     uint amountOwing = amounts[i].add(premiums[i]);
        //     IERC20(assets[i]).approve(address(POOL), amountOwing);
        // }
        return true;
    }
}

contract AaveFlashloanReceiverOk2 {
    address POOL;

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        if (msg.sender != POOL) {
            revert("not pool");
        }
        assert(initiator == address(this));

        //doing transfer
        // for (uint i = 0; i < assets.length; i++) {
        //     uint amountOwing = amounts[i].add(premiums[i]);
        //     IERC20(assets[i]).approve(address(POOL), amountOwing);
        // }
        return true;
    }
}

contract AaveFlashloanReceiverOk3 {
    address POOL;

    function _ensure_params(address initiator) internal {
        // if (msg.sender != POOL) {
        //     revert("not pool");
        // }
        assert(initiator == address(this));
    }

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        if (msg.sender != POOL) {
            revert("not pool");
        }
        _ensure_params(initiator);

        //doing transfer
        // for (uint i = 0; i < assets.length; i++) {
        //     uint amountOwing = amounts[i].add(premiums[i]);
        //     IERC20(assets[i]).approve(address(POOL), amountOwing);
        // }
        return true;
    }
}

contract AaveFlashloanReceiverOk3WithModifier {
    address POOL;
    modifier onlyThis() {
        require(msg.sender == POOL);
        _;
    }

    function _ensure_params(address initiator) internal {
        assert(initiator == address(this));
    }

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external onlyThis returns (bool) {
        _ensure_params(initiator);

        //doing transfer
        // for (uint i = 0; i < assets.length; i++) {
        //     uint amountOwing = amounts[i].add(premiums[i]);
        //     IERC20(assets[i]).approve(address(POOL), amountOwing);
        // }
        return true;
    }
}
