from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


class DoubleEntryTokenPossiblity(AbstractDetector):
    """
    Sees if contract contains a function which is vulnurable to double-entry tokens attack
    """

    ARGUMENT = 'pess-double-entry-token-alert' # slither will launch the detector with slither.py --detect mydetector
    HELP = 'The function might be sensitive to double entry token usage'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.LOW

    WIKI = 'https://github.com/pessimistic-io/slitherin/blob/master/docs/double_entry_token_possibility.md'
    WIKI_TITLE = 'Double-entry token'
    WIKI_DESCRIPTION = "Double-entry token related attack might be possible"
    WIKI_EXPLOIT_SCENARIO = '-'
    WIKI_RECOMMENDATION = 'Project contract must be sustainable to a token which has two pointing addresses'


    def get_tokens_as_params(self, fun):

        res = []  # параметры функции
        for p in fun.parameters:
            if len(p._name) and str(p.type) in ['IERC20[]', 'address[]']:
                res.append(p)

        return res

    def do_have_token_interaction(self, fun, token):

        for n in fun.nodes:
            if str(token) in str(n.expression):
                if '.transfer' in str(n.expression): return True
                if '.balanceOf' in str(n.expression): return True

        return False

    def _detect(self):

        res = []

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions:

                tokens = self.get_tokens_as_params(f)

                if len(tokens)>0:
                    for t in tokens:
                        if self.do_have_token_interaction(f, t):
                            res.append(self.generate_result([
                                f.contract_declarer.name, ' ',
                                f, ' might be vulnerable to double-entry token exploit',
                                '\n']))

        return res