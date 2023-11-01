from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from typing import List
from slither.core.cfg.node import Node
from slither.core.declarations import Function, SolidityVariableComposed
from slither.analyses.data_dependency.data_dependency import is_dependent


class NftApproveWarning(AbstractDetector):
    """
    Sees if contract contains erc721.[safe]TransferFrom(from, ...) where from parameter is not related to msg.sender
    """

    ARGUMENT = 'pess-nft-approve-warning' # slither will launch the detector with slither.py --detect nft-approve-warning
    HELP = '[safe]TransferFrom(from,...) - from parameter is not related to msg.sender'
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://ventral.digital/posts/2022/8/18/sznsdaos-bountyboard-unauthorized-transferfrom-vulnerability'
    WIKI_TITLE = 'NFT Approve Warning'
    WIKI_DESCRIPTION = "In [safe]TransferFrom() from parameter must be related to msg.sender"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'from parameter must be related to msg.sender'

    _signatures=["transferFrom(address,address,uint256)", "safeTransferFrom(address,address,uint256,bytes)", "safeTransferFrom(address,address,uint256)"]

    def _detect_arbitrary_from(self, f: Function):
        all_high_level_calls = [
            f_called[1].solidity_signature
            for f_called in f.high_level_calls
            if isinstance(f_called[1], Function)
        ]
        all_library_calls = [f_called[1].solidity_signature for f_called in f.library_calls]

        all_calls = all_high_level_calls + all_library_calls

        if (any(map(lambda s: s in all_calls, self._signatures))):
            return self._arbitrary_from(f.nodes)
        else:
            return []

    def _arbitrary_from(self, nodes: List[Node]):
        """Finds instances of (safe)transferFrom that do not use msg.sender or address(this) as from parameter."""
        irList = []
        for node in nodes:
            for ir in node.irs:
                if (
                    hasattr(ir, 'function')
                    and hasattr(ir.function, 'solidity_signature')
                    and ir.function.solidity_signature in self._signatures
                ):
                    is_from_sender = is_dependent(ir.arguments[0], SolidityVariableComposed("msg.sender"), node.function.contract)
                    # is_from_self = is_dependent(ir.arguments[0], SolidityVariable("this"), node.function.contract)
                    if (not is_from_sender): # and not is_from_self
                        irList.append(ir.node)
        return irList


    def _detect(self):
        """Detect transfers that use arbitrary `from` parameter."""
        res = []
        for c in self.compilation_unit.contracts_derived:
            for f in c.functions:
                for d in self._detect_arbitrary_from(f):
                    res.append(self.generate_result([f.contract_declarer.name, ' ',f.name, ' parameter from is not related to msg.sender ', d, '\n']))
        return res
