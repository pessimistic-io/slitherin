from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification

from typing import List
from slither.core.cfg.node import Node
from slither.core.declarations.solidity_variables import SolidityVariable
from slither.slithir.operations import LibraryCall
from slither.core.declarations import Contract, Function, SolidityVariableComposed
from slither.analyses.data_dependency.data_dependency import is_dependent


class NftApproveWarning(AbstractDetector):
    """
    Sees if contract contains erc721.[safe]TransferFrom(from, ...) where from parameter is not related to msg.sender
    """

    ARGUMENT = 'nft-approve-warning' # slither will launch the detector with slither.py --detect nft-approve-warning
    HELP = '[safe]TransferFrom(from,...) - from parameter is not related to msg.sender'
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = 'https://ventral.digital/posts/2022/8/18/sznsdaos-bountyboard-unauthorized-transferfrom-vulnerability'
    WIKI_TITLE = 'NFT Approve Warning'
    WIKI_DESCRIPTION = "В [safe]TransferFrom() параметр from должен сравниваться с msg.sender"
    WIKI_EXPLOIT_SCENARIO = 'Атакующий мог забрать любые nft, на который пользователь дал апрув протоколу. Причина: оптимистичный код erc721.safeTransferFrom(erc721.ownerOf(id),...) вместо erc721.safeTransferFrom(msg.sender,...) '
    WIKI_RECOMMENDATION = 'Параметр from должен быть msg.sender'


    def _detect_arbitrary_from(self, f: Function):
        all_high_level_calls = [
            f_called[1].solidity_signature
            for f_called in f.high_level_calls
            if isinstance(f_called[1], Function)
        ]
        all_library_calls = [f_called[1].solidity_signature for f_called in f.library_calls]
        if (
            "transferFrom(address,address,uint256)" in all_high_level_calls
            or "safeTransferFrom(address,address,address,uint256)" in all_library_calls
        ):
            x = NftApproveWarning._arbitrary_from(f.nodes)
            return x

    @staticmethod
    def _arbitrary_from(nodes: List[Node]):
        """Finds instances of (safe)transferFrom that do not use msg.sender or address(this) as from parameter."""
        irList = []
        for node in nodes:
            for ir in node.irs:
                if (ir.function.solidity_signature == "transferFrom(address,address,uint256)"):
                    if(is_dependent(ir.arguments[0], SolidityVariableComposed("msg.sender"),node.function.contract) == False or is_dependent(ir.arguments[0], SolidityVariable("this"), node.function.contract) == False):
                        irList.append(ir.node)
                        #return ir.node
                elif (
                    isinstance(ir, LibraryCall)
                    and ir.function.solidity_signature
                    == "safeTransferFrom(address,address,address,uint256)"
                    and not (
                        is_dependent(
                            ir.arguments[1],
                            SolidityVariableComposed("msg.sender"),
                            node.function.contract,
                        )
                        or is_dependent(
                            ir.arguments[1],
                            SolidityVariable("this"),
                            node.function.contract,
                        )
                    )
                ):
                    #return ir.node
                    irList.append(ir.node)
        return irList

    def _detect(self):
        """Detect transfers that use arbitrary `from` parameter."""
        res = []
        i = 0
        for c in self.compilation_unit.contracts_derived:
            for f in c.functions:
                x = self._detect_arbitrary_from(f)
                if(x != None):
                    xLen = len(x)
                    while(i < xLen):
                        res.append(self.generate_result([f.contract_declarer.name, ' ',f.name, ' parameter from is not related to msg.sender ', x[i], '\n']))
                        i = i+1
                        print(res)

        return res