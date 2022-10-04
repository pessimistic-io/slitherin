from slither.core.cfg.node import NodeType
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


class StrangeSetter(AbstractDetector):
    """
    Sees if contract contains a setter, that does not change contract storage variables
    """

    ARGUMENT = 'strange-setter' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'Contract storage parameter is not changed by setter'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = 'https://workflowy.com/#/692cf11bd6f1'
    WIKI_TITLE = 'Strange Setter'
    WIKI_DESCRIPTION = "Сеттеры должны менять значения storage переменных"
    WIKI_EXPLOIT_SCENARIO = 'Неработающий контракт'
    WIKI_RECOMMENDATION = 'Fix setter function'


    def is_strange_setter(self, fun, params=None):

        if not params:
            params = fun.parameters # параметры функции

        for n in fun.nodes: # в первом приближении нода это строчка
            if(n.type==NodeType.EXPRESSION):
                for v in n.state_variables_written:
                    lr = str(n.expression).split(' = ')
                    if len(lr)>1:
                        left = lr[0]
                        right = lr[1]
                        for p in params:
                            if '.' in left: continue
                            if '[' in left: continue
                            if right==str(p):
                                return left # присваеваем аргумент функции напрямую в сторадж

        # TODO: непрямые присваивания
        return "None"

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:
                if(f.name.startswith("set")):
                    x = self.is_strange_setter(f)
                    if (x == "None"):
                        res.append(self.generate_result([
                            f.contract_declarer.name, ' ',
                            f.name, ' is a strange setter ',
                            x, ' is set'
                            '\n']))


        return res