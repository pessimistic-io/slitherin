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
}
