pragma solidity ^0.8.13;

contract multiple_storage_read_test {
    uint256 var1 = 100;
    uint256 var2 = 200;
    uint256 result_add;
    uint256 result_substract;
    uint256 result_mul;
    uint256 result_div;


    function calculate_vulnurable() external {
        var1 = var1 + var2;
        result_substract = var2 - var1;
        result_mul = var1*var2;
        result_div = var2/var1;
    }

    function calculate_ok() external {
        uint256 var1_local = var1;
        uint256 var2_local = var2;
        result_add = var1_local + var2_local;
        result_substract = var2_local - var1_local;
        result_mul = var1_local*var2_local;
        result_div = var2_local/var1_local;
    }
}
