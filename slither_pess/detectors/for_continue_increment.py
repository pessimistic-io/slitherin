from typing import List, Optional
from slither.core.cfg.node import NodeType, Node
from slither.core.declarations import Contract, Function
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output


class Context():
    def __init__(self):
      self.visited = []
      self.depth = 0
      self.index_var = None
      self.father_type = None
      self.continue_seen = False
      self.checked_increase = False # necessary condition is the absence of a checked increase.
      self.unchecked_increase = False # Used to detect when the unchecked{i++} happens before the continue statement (false pos to filter out).
      #                                 We use this also in the case of [continue, break, return] at the end of the loop body, in such case the 
      #                                 presence of an unchecked increase is required.
      
    def __str__(self): # debug
        return 'index_var: ' + str(self.index_var) + ' - continue: ' + str(self.continue_seen) + ' - checked_increase: ' + str(self.checked_increase)


def check_contract(c: Contract) -> List[Function]:
  results_raw: List[Function] = []

  # skip test contracts
  if any(x in c.name for x in ["Test", "Mock"]): 
    return results_raw

  # filter unwanted funcs
  to_inspect = (x for x in c.functions if x.is_implemented)

  for f in to_inspect: 
    if check_function(f.entry_point, Context()):
      results_raw.append(f)
  return results_raw


def check_function(node: Optional[Node], ctx: Context)-> bool:
  if node is None: 
    return []

  if node in ctx.visited:
    return []
  ctx.visited.append(node)
  
  # continue_seen flag
  if node.type == NodeType.CONTINUE and ctx.index_var is not None and not ctx.unchecked_increase: # ctx.index_var is not None makes sure we are inside the loop
    ctx.continue_seen = True

  # set loop index variable
  if node.type == NodeType.STARTLOOP:
    if len(node.fathers) > 0: # should always be true
      main_father = node.fathers[0] 
      local_written = main_father.local_variables_written 
      if not len(local_written): # this happens if the index is left implicitly to 0 e.g. for (uint i; i < ...
        local_written = [main_father.variable_declaration] # in this case we get the declared one
      if len(local_written) == 1: # should always be true
        ctx.index_var = local_written[0] # strong assumption, it might be wrong in weird situations

  # check increase flag
  if node.type == NodeType.EXPRESSION and ctx.index_var is not None:
    local_written = node.local_variables_written
    if ctx.index_var in local_written: 
      if node.scope.is_checked:
        ctx.checked_increase = True
      else:
        ctx.unchecked_increase = True

  # if end_loop and not index increased, return true
  if node.type == NodeType.ENDLOOP:
    if ctx.index_var is not None and ctx.continue_seen and not ctx.checked_increase:
      if ctx.father_type in [NodeType.BREAK, NodeType.RETURN, NodeType.CONTINUE]:
        if ctx.unchecked_increase:
          return True
      else:
        return True 
    else:
      # clean the context for the next loop if any
      ctx.index_var = None 
      ctx.continue_seen = False 
      ctx.checked_increase = False

  # if didn't return true, inspect sons
  ctx.father_type = node.type
  ret = False
  for son in node.sons:
    ret = ret or check_function(son, ctx) # ctx passed by reference to collect 'continue_seen' and 'checked_increase' flags among all the previous branches
  return ret


class ForContinueIncrement(AbstractDetector):

    ARGUMENT = "pess-for-continue-increment" # slither will launch the detector with slither.py --detect for-continue-increment
    HELP = "Loop might turn out infinite"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.LOW

    WIKI = "https://github.com/sherlock-audit/2023-02-olympus-judging/issues/125"

    WIKI_TITLE = "For continue increment"
    WIKI_DESCRIPTION = "A continue statement before an unchecked index increment can turn into an infinite loop"
    WIKI_EXPLOIT_SCENARIO = "-"
    WIKI_RECOMMENDATION = "Increment the loop index before the continue statement"

    def _detect(self) -> List[Output]:
      """"""
      results: List[Output] = []
      results_raw: List[Function] = []
      for c in self.compilation_unit.contracts_derived:
        results_raw += check_contract(c)

      for sl in results_raw:
        info = [
          f"Found vulnerable for loop in function '",
          sl,
          "'\n"
        ]
        res = self.generate_result(info)
        results.append(res)

      return results         

