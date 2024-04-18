from typing import List
from slither.utils.output import Output
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.slithir.operations.high_level_call import HighLevelCall
from slither.slithir.operations.internal_call import InternalCall
from slither.slithir.operations.solidity_call import SolidityCall
from slither.slithir.operations.binary import Binary
from slither.analyses.data_dependency.data_dependency import is_dependent


class PriceManipulationDetector(AbstractDetector):
    ARGUMENT = 'pess-price-manipulation' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract math can be manipulated through external token transfers.'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/price_manipulation.md'
    WIKI_TITLE = '# Price Manipulation through token transfers'
    WIKI_DESCRIPTION = "Calculations could be manipulated through direct transfers to the contract, increasing its balance as they depends on these balances."
    WIKI_EXPLOIT_SCENARIO = 'N/A'
    WIKI_RECOMMENDATION = 'Avoid possible manipulations of calculations because of external transfers.'

    def _detect(self) -> List[Output]:
        all_balance_vars = []
        all_supply_vars = []
        all_binary_ops = []
        for contract in self.contracts:
            if not contract.is_interface:
                for func in contract.functions:
                    for n in func.nodes:
                        for x in n.irs:
                            if isinstance(x, SolidityCall):
                                if x.function.name == "balance(address)" or x.function.name == "self.balance" or x.function.name == "this.balance()":
                                    all_balance_vars.append((n, x._lvalue))
                            if isinstance(x, HighLevelCall):
                                if str(x.function_name).lower() == "balanceof":
                                    all_balance_vars.append((n, x._lvalue))
                                if "supply" in str(x.function_name).lower():
                                    all_supply_vars.append((n, x._lvalue))
                            if isinstance(x, InternalCall):
                                if "supply" in str(x.function_name).lower():
                                    all_supply_vars.append((n, x._lvalue))
                            if isinstance(x, Binary):
                                all_binary_ops.append((n, x))
        results = []
        for (balance_node, bal) in all_balance_vars:
            for (supply_node, supply) in all_supply_vars:
                for (node, bin_op) in all_binary_ops:
                    l, r = bin_op.get_variable
                    is_bal_dependent = is_dependent(l, bal, contract)
                    is_supply_dependent = is_dependent(r, supply, contract)
                    if is_bal_dependent and is_supply_dependent:
                        results.append((node, balance_node, supply_node))
        if not results:
            return []
        
        
        response = []
        for issue_node, balance_node, supply_node in results:
            res = []
            res.append("Calculation ")
            res.append(issue_node)
            res.append(" depends on balance and token supply - these values could be manipulated through external calls.\n")
            res.append("\tBalance dependency: ")
            res.append(balance_node)
            res.append("\n")
            res.append("\tSupply dependency: ")
            res.append(supply_node)
            res.append("\n")
            response.append(self.generate_result(res))
        return response
