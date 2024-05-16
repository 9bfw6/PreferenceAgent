from pysat.formula import CNF
from pysat.solvers import Solver


class QualitativeChoiceLogic:
    """
    This class represents an instance of a Qualitative Choice logic rule from theory T.

    Attributes:
    - name (str): The name of the rule.
    - constraints (list): The different preference options of each rule. φ
    - condition (list): The condition of each rule. ψ
    """

    def __init__(self, name, constraints, condition):
        """
        Initializes a new qualitative choice logic rule.

        :param name (str): The rule as a string.
        :param constraints (list): The different preference options of each rule. φ
        :param condition (list): The condition of each rule. ψ
        """
        self.name = name
        self.constraints = constraints
        self.condition = condition

    def test(self, test_object):
        """
        Applies qualitative choice logic rule on feasible object test_object.

        :param test_object (Object): The feasible object being tested.
        :return (int): The satisfaction degree of logic rule for feasible object test_object.
        """
        logic_values = {}
        true_logics = []
        condition_value = False
        pysat_formulas = []
        condition_formula = self.condition
        logics = self.constraints.copy()
        object_test_integers = test_object.return_test_integers()
        inf = float('inf')

        for logic in logics:
            formula = logic.copy()
            for test_integer in object_test_integers:
                formula.append(test_integer)
            pysat_formulas.append(formula)

        if condition_formula is not None:
            test_condition = condition_formula.copy()
            for test_integer in object_test_integers:
                test_condition.append(test_integer)
            cnf = CNF(from_clauses=test_condition)
            with Solver(bootstrap_with=cnf) as solver:
                if solver.solve():
                    condition_value = True

        for index, pysat_formula in enumerate(pysat_formulas, 1):  # test each logic and store as true or false
            cnf = CNF(from_clauses=pysat_formula)
            with Solver(bootstrap_with=cnf) as solver:
                if solver.solve():
                    value = True
                    logic_values[index] = value
                else:
                    value = False
                    logic_values[index] = value

        for key in logic_values:
            if logic_values[key]:
                true_logics.append(key)

        if condition_value:
            if true_logics:
                minimum = min(true_logics)
                return minimum
            else:
                return inf
        else:
            if condition_formula is not None:
                return inf
            else:
                if true_logics:
                    minimum = min(true_logics)
                    return minimum
                else:
                    return inf

    def get_name(self):
        """
        Returns the name of the logic rule.

        :return (str): name.
        """
        return self.name
