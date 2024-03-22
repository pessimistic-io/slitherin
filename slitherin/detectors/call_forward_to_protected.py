from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations import LowLevelCall
from slither.core.declarations import Function
from slither.utils.output import Output
from pathlib import Path
from typing import List

OZ_EXCLUDED_CONTRACTS_SUFFIXES: List[str] = [
    "contracts/utils/Address.sol",
    "contracts-upgradeable/utils/AddressUpgradeable.sol",
    "contracts/utils/AddressUpgradeable.sol",
    "contracts/token/ERC20/utils/SafeERC20.sol"
]

UNISWAP_EXCLUDED_CONTRACTS_SUFFIXES: List[str] = [
    "lib/contracts/libraries/TransferHelper.sol"
]

BALANCER_EXCLUDED_CONTRACTS_SUFFIXES: List[str] = [
    "v2-solidity-utils/contracts/openzeppelin/SafeERC20.sol"
]
class CallForwardToProtected(AbstractDetector):
    """
    Shows cases when contract calls custom addresses and has contract interactions through access control
    """

    ARGUMENT = 'pess-call-forward-to-protected' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract might have a call to a custom address'
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/call_forward_to_protected.md'
    WIKI_TITLE = 'Call Forward To Protected'
    WIKI_DESCRIPTION = "No calls to custom addresses and contract interactions through access control"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Do not let calls to project contracts or do not give rights to a contract which can perform calls'

    
    def _contains_low_level_calls(self, node) -> bool:
        return any(isinstance(ir, LowLevelCall) for ir in node.irs)

    def _detect_low_level_custom_address_call(self, fun: Function) -> bool:
        address_parameters = [
            parameter for parameter in fun.parameters if str(parameter.type) == "address" and parameter.name
        ]
        for node in fun.nodes:
            if self._contains_low_level_calls(node):
                for address_parameter in address_parameters:
                    if str(address_parameter) in str(node):
                        return True
        return False
    
    def _pess_is_excluded_from_detector(self, contract: "Contract") -> bool:
        path = Path(contract.source_mapping.filename.absolute).parts
        is_zep = "openzeppelin-solidity" in path or \
                    ("@openzeppelin" in path and path[path.index("@openzeppelin") + 1] == "contracts") or \
                    "openzeppelin-contracts-upgradeable" in path or \
                    ("@openzeppelin-contracts-upgradeable" in path and \
                        (path[path.index("@openzeppelin-contracts-upgradeable") + 1] == "contracts" or \
                         path[path.index("@openzeppelin-contracts-upgradeable") + 1] == "contracts-upgradeable"))

        if is_zep:
            return any(map(lambda suffix: contract.source_mapping.filename.absolute.endswith(suffix), OZ_EXCLUDED_CONTRACTS_SUFFIXES)) 
        elif "@uniswap" in path:
            return any(map(lambda suffix: contract.source_mapping.filename.absolute.endswith(suffix), UNISWAP_EXCLUDED_CONTRACTS_SUFFIXES)) 
        elif "@balancer-labs" in path: 
            return any(map(lambda suffix: contract.source_mapping.filename.absolute.endswith(suffix), BALANCER_EXCLUDED_CONTRACTS_SUFFIXES)) 
        return False

    def _detect(self) -> List[Output]:
        res = []
        for contract in self.compilation_unit.contracts_derived:
            if self._pess_is_excluded_from_detector(contract):
                continue
            for f in contract.functions:
                x = self._detect_low_level_custom_address_call(f)
                if x:
                    res.append(self.generate_result([
                            "Function", ' ',
                            f, ' contains a low level call to a custom address',
                            '\n']))

        return res
