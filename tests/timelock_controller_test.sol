// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;
import "../node_modules/@openzeppelin/contracts/governance/TimelockController.sol";

contract timelock_controller_test {
    TimelockController public timelockController;
    constructor(TimelockController _timelockController){
        timelockController = _timelockController;
    }

    function check_role (address _address_proposer) external view returns (bool) {
        bytes32 prop_role = timelockController.PROPOSER_ROLE(); 
        bool boolean = timelockController.hasRole(prop_role, _address_proposer);
        return boolean;
    }
}