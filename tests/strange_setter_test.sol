pragma solidity ^0.8.0;

contract StrangeSetter {
    uint256 toSet;
    bool isProtected = true;
    mapping(bytes32 => address) s_builders;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    constructor(uint256 _setter){
        toSet = _setter;
    }

    function set_vulnurable(uint256 setter) public onlyOwner {
        uint256 a = 10;
        a = setter;
    }

    function set_vulnurable_mapping(uint256 _toSet) external onlyOwner {
        uint256 vars = _toSet;
        toSet = vars;
    }

    function setBuilder(bytes32 nameHash, address builder) public onlyOwner{
        s_builders[nameHash] = builder;
    }

    function setWithInt(bytes32 nameHash, address builder) public onlyOwner{
        uint256 x = 0;
        vulnurable_internal(x);
    }

    function set_ok(uint256 setter) public onlyOwner {
        toSet = setter;
    }

    function vulnurable_internal(uint256 setter) internal {
        toSet = setter;
    } 
}

contract StrangeConstructor {
    uint256 toSet;

    constructor(uint256 _setter){
        uint256 local_set;
        local_set = _setter + 10;
    }
}

contract OkConstructor {    //if constructor has no parameters or is empty - do not detect
    constructor(){}
}

