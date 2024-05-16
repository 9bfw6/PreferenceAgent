from pysat.formula import CNF
from pysat.solvers import Solver


class PenaltyLogic:
    """
    This class represents an instance of a penalty logic rule.

    Attributes:
    - name (str): The name of the rule as a string.
    - constraint (list): The rule as a list.
    - penalty (int): The penalty associated with this rule.
    """
    def __init__(self, name, constraint, penalty):
        """
        Initializes a new penalty logic rule.

        :param name (str): The name of the rule as a string.
        :param constraint (list): The rule as a list.
        :param penalty (int): The penalty associated with this rule.
        """
        self.name = name
        self.constraint = constraint
        self.penalty = penalty

    def test(self, test_object):
        """
        Applies penalty logic rule on feasible object test_object.
        :param test_object (Object): The feasible object being tested.
        :return (int): The penalty applied to test_object.
        """
        test_formula = self.constraint.copy()
        penalty = self.penalty
        object_test_integers = test_object.return_test_integers()
        for obj_integer in object_test_integers:
            test_formula.append(obj_integer)
        cnf = CNF(from_clauses=test_formula)
        with Solver(bootstrap_with=cnf) as solver:
            if solver.solve():
                penalty = 0
                test_object.add_penalty(penalty)
            else:
                test_object.add_penalty(penalty)
        return penalty

    def get_name(self):
        """
        Returns the rule instance as a string.
        :return (str): name.
        """
        return self.name
