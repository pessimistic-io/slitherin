from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.core.declarations import Function


class TxGaspriceWarning(AbstractDetector):
    """
    Sees if contract function uses variable tx.gasprice.
    """

    ARGUMENT = 'pess-tx-gasprice' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'The contract uses tx.gasprice variable'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/tx_gasprice_warning.md'
    WIKI_TITLE = 'TX Gasprice Warning'
    WIKI_DESCRIPTION = "Tx.gasprice variable must be used carefully"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Make sure that tx.gasprice varible which is set by users does not exploit the contract logic'


    def _has_tx_gasprice(self, fun: Function) -> bool: 
        """Checks if function has tx.gasprice variable"""
        if isinstance(fun, Function):   # check for a correct function type
            for n in fun.nodes: # checks every node for a tx.gasprice variable
                if "tx.gasprice" in str(n):
                    return True
        return False


    def _detect(self) -> List[Output]:
        """Main function"""
        res = []
        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions_and_modifiers_declared:
                x = self._has_tx_gasprice(f)
                if x:
                    res.append(self.generate_result([
                        "In a function ",
                        f, ' tx.gasprice (which is set by user) variable is used. Make sure that it can not exploit the contract logic.',
                        '\n']))
        return res
