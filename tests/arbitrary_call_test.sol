interface IERC20 {
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);
}

contract Test {
    address toAddress;
    bytes callData;

    function _makeCall(address to, bytes memory data) private {
        //This is not vulnarable by itself
        to.call(data);
    }

    function _makeCall2(address to) private {
        to.call(callData);
    }

    function _makeCall3(bytes memory data) private {
        toAddress.call(data);
    }

    function _makeCall4(bytes memory data) private {
        toAddress.call(abi.encodePacked(callData, data));
    }

    function _makeCallToThis(bytes memory data) private {
        address(this).call(data);
    }

    function _makeCallNoData(address to) private {
        to.call("");
    }

    function publicCallArbitraty(address to, bytes memory data) public {
        //This is vulnerable
        _makeCall(to, data);
        _makeCall2(to);
        _makeCall3(data);
        _makeCall4(data);
        _makeCallToThis(data);
        _makeCallNoData(to);
    }

    function calldataHalfManipulated(bytes memory data) public {
        bytes4 selector = 0xffffffff;
        bytes memory _calldata = abi.encodeWithSelector(selector, data);
        //this will also be considered as fully vulnerable, even though user cannot fully manipulate the calldata
        _makeCall3(data);
    }

    function publicNonArbitraryCall() public {
        //This is not vulnerable
        _makeCall(toAddress, callData);
    }

    function semiArbitraryCall(address to) external {
        _makeCall(to, callData);
    }

    function semiArbitraryCall2(bytes calldata data) external {
        _makeCall(toAddress, data);
    }

    function assembly_delegateCall_full_tainted(
        address target,
        address data
    ) public returns (bytes memory response) {
        // call contract in current context
        bytes memory _data = abi.encodeWithSignature("relay(address)", data);
        assembly {
            let succeeded := delegatecall(
                sub(gas(), 5000),
                target,
                add(_data, 0x20),
                mload(_data),
                0,
                0
            )
            let size := returndatasize()

            response := mload(0x40)
            mstore(
                0x40,
                add(response, and(add(add(size, 0x20), 0x1f), not(0x1f)))
            )
            mstore(response, size)
            returndatacopy(add(response, 0x20), 0, size)

            switch iszero(succeeded)
            case 1 {
                // throw if delegatecall failed
                revert(add(response, 0x20), size)
            }
        }
    }

    function assembly_delegateCall_only_data_tainted(
        address data
    ) public returns (bytes memory response) {
        // call contract in current context
        bytes memory _data = abi.encodeWithSignature("relay(address)", data);
        address target = toAddress;
        assembly {
            let succeeded := delegatecall(
                sub(gas(), 5000),
                target,
                add(_data, 0x20),
                mload(_data),
                0,
                0
            )
            let size := returndatasize()

            response := mload(0x40)
            mstore(
                0x40,
                add(response, and(add(add(size, 0x20), 0x1f), not(0x1f)))
            )
            mstore(response, size)
            returndatacopy(add(response, 0x20), 0, size)

            switch iszero(succeeded)
            case 1 {
                // throw if delegatecall failed
                revert(add(response, 0x20), size)
            }
        }
    }

    function assembly_call_full_tainted(
        address target,
        address data
    ) public returns (bytes memory response) {
        // call contract in current context
        bytes memory _data = abi.encodeWithSignature("dosmth(address)", data);
        assembly {
            let succeeded := call(
                sub(gas(), 5000),
                target,
                0,
                add(_data, 0x20),
                mload(_data),
                0,
                0
            )
            let size := returndatasize()

            response := mload(0x40)
            mstore(
                0x40,
                add(response, and(add(add(size, 0x20), 0x1f), not(0x1f)))
            )
            mstore(response, size)
            returndatacopy(add(response, 0x20), 0, size)

            switch iszero(succeeded)
            case 1 {
                // throw if delegatecall failed
                revert(add(response, 0x20), size)
            }
        }
    }
}

contract TestWithApprove {
    function swap(IERC20 token) external {
        token.transferFrom(msg.sender, address(this), 1);
    }

    function call(address to, bytes memory data) public {
        to.call(data);
    }
}
