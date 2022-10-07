from slither.core.declarations import SolidityVariableComposed, SolidityFunction, SolidityVariable
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.analyses.data_dependency.data_dependency import is_dependent


class DangerousBalanceTransfer(AbstractDetector):
    """
    Sees if contract contains a transfer of 90%+ contract balance
    """

    ARGUMENT = 'dangerous-balance-transfer' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract has a transfer of its balance'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://workflowy.com/#/6310b3446674'
    WIKI_TITLE = 'Dangerous Balance Transfer'
    WIKI_DESCRIPTION = "Contract balance can become 0"
    WIKI_EXPLOIT_SCENARIO = 'Contract transfers all its balance to a malicious address'
    WIKI_RECOMMENDATION = 'Be careful with contract balance transfers'


    def is_dangerous_balance_transfer(self, fun):
        for n in fun.nodes: # в первом приближении нода это строчка
            for ir in n.irs:
                if(ir.function.solidity_signature == "transfer(address,uint256)"):
                    if(str(ir.expression).__contains__('transfer')):
                        expressionString = str(ir.expression)
                        if(expressionString.__contains__('balanceOf' or 'this')):
                            return "True"
                        #TODO Relations to balanceOf(address(this))
                        # print(expressionString)
                        # indx1 = expressionString.index(',')
                        # indx2 = expressionString.index(')')
                        # res = ''
                        # for idx in range(indx1 + len(','), indx2):
                        #     res = res + expressionString[idx]
                        # if(is_dependent(res, SolidityFunction("balance(address)"), n.function.contract)):
                        #     return "True"
                #if(expressionString)
                    #print(ir.function)
                    # print(ir.expression)
                    # return "True"

        return "False"

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                x = self.is_dangerous_balance_transfer(f)
                if (x == "True"):
                    res.append(self.generate_result([
                        f.contract_declarer.name, ' ',
                        f.name, ' has a dangerous balance transfer with dependence on balanceOf contract'
                        '\n']))


        return res