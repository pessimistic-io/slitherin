pragma solidity ^0.8.0;

interface ExternalContract {
    function set(bool arg) external;
}
// What it should detect:
// If smth is set in the function, and the function contains parameters,
// and this parameters were not uset to set.
contract StrangeSetter {
    uint256 toSet;
    bool isProtected = true;
    mapping(bytes32 => address) s_builders;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    constructor(uint256 _setter) {
        toSet = _setter;
    }

    function set_vulnurable(uint256 setter) public onlyOwner {
        uint256 a = 10;
        a = setter;
    }

    function set_vulnurable_shadowing(uint256 setter) public onlyOwner {
        uint256 setter = 2; //TODO: THIS IS NOT DETECTED!!!
        toSet = setter;
    }

    function set_vulnerable_mapping(uint256 _toSet) external onlyOwner {
        uint256 vars = _toSet;
        toSet = vars;
    }

    function setBuilder(bytes32 nameHash, address builder) public onlyOwner {
        s_builders[nameHash] = builder;
    }

    function setWithInt(bytes32 nameHash, address builder) public onlyOwner {
        uint256 x = 0;
        vulnurable_internal(x);
    }

    function setSwapEnabledExternal_ok(ExternalContract target, bool swapEnabled) external onlyOwner {
        target.set(swapEnabled);
    }

    function setUseOnlyOneArg_vulnerable(uint256 arg1, bool isProtectedArg) external onlyOwner {
        isProtected = isProtectedArg;
    }

    function set_ok(uint256 setter) public onlyOwner {
        toSet = setter;
    }

    function set_ok_with_temp_war(uint256 setter) public onlyOwner {
        uint k = setter * 100;
        toSet = k;
    }

    function vulnurable_internal(uint256 setter) internal {
        toSet = setter;
    }
}

contract StrangeConstructor {
    uint256 toSet;

    constructor(uint256 _setter) {
        uint256 local_set;
        local_set = _setter + 10;
    }
}

contract OkConstructor {
    bool init;

    //if constructor has no parameters or is empty - do not detect
    constructor() {
        disableInitializers();
    }

    function disableInitializers() internal {
        init = true;
    }
}

contract TestInheritance is StrangeSetter{
    constructor(uint256 _toSet) StrangeSetter(_toSet) {}
}

contract TestNewContract {
    constructor(uint256 _toSet) {
        new TestInheritance(_toSet);
    }
}