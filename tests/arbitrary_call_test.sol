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

    function publicCallArbitraty(address to, bytes memory data) public {
        //This is vulnerable
        _makeCall(to, data);
        _makeCall2(to);
        _makeCall3(data);
        _makeCall4(data);
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
}
