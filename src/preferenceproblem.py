from pysat.formula import CNF
from pysat.solvers import Solver
from prettytable import PrettyTable
from random import sample


class PreferenceProblem:
    """
    This class represents a new preference logic problem.

    Attributes:
    - objects (list): The objects of the preference logic problem.
    - hard_constraints (list): The hard constraints of the preference logic problem.
    - penalty_logics (list): The penalty logic rules of the preference logic problem.
    - qualitative_logics (list): The qualitative choice logic rules of the preference logic problem.
    - feasible_objects (list): A list of the problem's feasible objects.
    - check_feasibility(): Processes the feasible objects of the preference problem.
    - penalty_logic_table (PrettyTable): A PrettyTable storing penalty logic data.
    - qualitative_choice_table (PrettyTable): A PrettyTable storing qualitative choice logic data.

    """

    def __init__(self, objects, hard_constraints, penalty_logics, qualitative_logics):
        """
        Initializes A new preference logic problem.

        :param objects (list): A list of Object instances.
        :param hard_constraints (list): A list of hard constraint formulas.
        :param penalty_logics (list): A list of penalty logic rule instances.
        :param qualitative_logics (list): A list of qualitative choice logic rule instances.
        """
        self.objects = objects
        self.hard_constraints = hard_constraints
        self.penalty_logics = penalty_logics
        self.qualitative_logics = qualitative_logics
        self.object_qualitative_values = {}
        self.feasible_objects = []
        self.check_feasibility()
        self.penalty_logic_table = self.apply_penalty_logic()
        self.qualitative_choice_table = self.apply_qualitative_choice_logic()

    def encoding(self):
        """
        Displays each encoded object.

        :return: None.
        """
        for obj in self.objects:
            obj.__str__()

    def check_feasibility(self):
        """
        Calculates the number of feasible objects.

        :return: None.
        """
        valid_objects = []
        cnf = CNF(from_clauses=self.hard_constraints)
        with Solver(bootstrap_with=cnf) as solver:
            for m in solver.enum_models():
                valid_objects.append(m)
            for obj in self.objects:
                if obj.return_integer_values() in valid_objects:
                    self.feasible_objects.append(obj)

    def return_feasibility(self):
        """
        Displays the number of feasible objects to the user.

        :return: None.
        """
        if self.feasible_objects:
            number_of_feasible_objects = len(self.feasible_objects)
            print(f"Yes, there are {number_of_feasible_objects} feasible objects.")
        else:
            print("No feasible objects.")

    def apply_penalty_logic(self):
        """
        Applies penalty logic on the feasible objects of the problem, and creates the
        penalty logic table.

        :return (PrettyTable): The penalty logic table.
        """
        columns = self.make_penalty_table_columns()
        my_table = PrettyTable(columns)
        for obj in self.feasible_objects:
            row = [obj.get_name()]
            for penalty_logic in self.penalty_logics:
                penalty = penalty_logic.test(obj)
                row.append(penalty)
            row.append(obj.get_total_penalty())
            my_table.add_row(row)
        return my_table

    def apply_qualitative_choice_logic(self):
        """
        Applies qualitative choice logic on the feasible objects of the problem, and
        creates the qualitative choice logic table.

        :return (PrettyTable): The qualitative choice logic table.
        """
        columns = self.make_qualitative_table_columns()
        my_table = PrettyTable(columns)
        infinity = float('inf')
        for obj in self.feasible_objects:
            row = [obj.get_name()]
            qualitative_values = []
            for qualitative_logic in self.qualitative_logics:
                value = qualitative_logic.test(obj)
                row.append(value)
                if value == infinity:
                    value = 10000  # finite number to represent infinity, so that optimal objects can be found
                qualitative_values.append(value)
            my_table.add_row(row)
            self.object_qualitative_values[obj.get_name()] = qualitative_values
        return my_table

    def penalty_exemplification(self):
        """
        Selects 2 random feasible objects, calculates the preference between them according
        to the penalty logic of the problem, and displays that information to the user.

        :return: None.
        """
        random_feasible_objects = sample(self.feasible_objects, 2)
        object_one = random_feasible_objects[0]
        object_two = random_feasible_objects[1]
        object_one_penalty = object_one.get_total_penalty()
        object_two_penalty = object_two.get_total_penalty()
        print(f"Two randomly selected feasible objects are {object_one.get_name()} and {object_two.get_name()},")
        if object_one_penalty > object_two_penalty:
            print(f"and {object_two.get_name()} is strictly preferred over {object_one.get_name()}.")
        elif object_two_penalty > object_one_penalty:
            print(f"and {object_one.get_name()} is strictly preferred over {object_two.get_name()}.")
        else:
            print(f"{object_one.get_name()} and {object_two.get_name()} are equivalent.")

    def penalty_omni_optimization(self):
        """
        Calculates all optimal, feasible objects according to the penalty logic of
        the problem, and displays them to the user.

        :return: None.
        """
        optimal_objects = []

        for obj in self.feasible_objects:
            if self.is_optimal_penalty_object(obj):
                optimal_objects.append(obj.get_name())

        output_string = ", ".join(optimal_objects)
        print(f"All optimal objects: {output_string}")

    def make_penalty_table_columns(self):
        """
        Makes and returns the columns for the penalty logic PrettyTable.

        :return (list): The columns of the PrettyTable.
        """
        columns = ["encoding"]
        for penalty_logic in self.penalty_logics:
            columns.append(penalty_logic.get_name())
        columns.append("total penalty")
        return columns

    def make_qualitative_table_columns(self):
        """
        Makes and returns the columns for the qualitative choice logic PrettyTable.

        :return (list): The columns of the PrettyTable.
        """
        columns = ["encoding"]
        for qualitative_logic in self.qualitative_logics:
            columns.append(qualitative_logic.get_name())
        return columns

    def qualitative_exemplification(self):
        """
        Selects 2 random feasible objects, calculates the preference between them according
        to the qualitative choice logic of the problem, and displays that information
        to the user.

        :return: None.
        """
        random_feasible_objects = sample(self.feasible_objects, 2)
        object_one = random_feasible_objects[0]
        object_two = random_feasible_objects[1]
        object_one_satisfaction_degrees = []
        object_two_satisfaction_degrees = []
        satisfaction_comparison = []
        print(f"Two randomly selected feasible objects are {object_one.get_name()} and {object_two.get_name()},")

        for key in self.object_qualitative_values:
            if key == object_one.get_name():
                object_one_satisfaction_degrees = self.object_qualitative_values[key].copy()
            elif key == object_two.get_name():
                object_two_satisfaction_degrees = self.object_qualitative_values[key].copy()

        for index, object_one_degree in enumerate(object_one_satisfaction_degrees):
            object_two_degree = object_two_satisfaction_degrees[index]
            if object_one_degree <= object_two_degree and object_one_degree < object_two_degree:
                satisfaction_comparison.append(1)
            elif object_one_degree >= object_two_degree and object_one_degree > object_two_degree:
                satisfaction_comparison.append(2)
            else:
                satisfaction_comparison.append(0)

        if 1 in satisfaction_comparison:
            if 2 in satisfaction_comparison:
                print(f"and {object_one.get_name()} and {object_two.get_name()} are incomparable.")
            else:
                print(f"and {object_one.get_name()} is strictly preferred over {object_two.get_name()}.")
        elif 2 in satisfaction_comparison:
            if 1 in satisfaction_comparison:
                print(f"and {object_one.get_name()} and {object_two.get_name()} are incomparable.")
            else:
                print(f"and {object_two.get_name()} is strictly preferred over {object_one.get_name()}.")
        else:
            print(f"and {object_one.get_name()} and {object_two.get_name()} are equal.")

    def qualitative_omni_optimization(self):
        """
        Calculates all optimal, feasible objects according to the qualitative choice
        logic of the problem, and displays them to the user.

        :return: None.
        """
        preference_degrees = []
        optimal_objects = []

        # store each preference degree in a list
        for key in self.object_qualitative_values:
            obj = self.object_qualitative_values[key].copy()
            if self.is_optimal_qualitative_object(obj):
                optimal_objects.append(key)

        output_string = ", ".join(optimal_objects)
        print(f"All optimal objects: {output_string}")

    def print_penalty_table(self):
        """
        Prints the penalty logic PrettyTable to the user.

        :return: None.
        """
        print(self.penalty_logic_table)

    def print_qualitative_table(self):
        """
        Prints the qualitative choice logic PrettyTable to the user.

        :return: None.
        """
        print(self.qualitative_choice_table)

    def is_optimal_qualitative_object(self, obj1):
        """
        Checks if the feasible object meets the criteria for an optimal object
        according to the qualitative choice logic rules of the problem.

        :param obj1 (Object): The feasible object in consideration.
        :return (Boolean): True if optimal, False otherwise.
        """
        is_optimal = True
        for key in self.object_qualitative_values:  # loop through object list to find optimal objects
            obj2 = self.object_qualitative_values[key].copy()

            satisfaction_comparison = []

            for index, object_one_degree in enumerate(obj1):  # compare objects
                object_two_degree = obj2[index]
                if object_one_degree <= object_two_degree and object_one_degree < object_two_degree:
                    satisfaction_comparison.append(1)
                elif object_one_degree >= object_two_degree and object_one_degree > object_two_degree:
                    satisfaction_comparison.append(2)
                else:
                    satisfaction_comparison.append(0)

            if 1 in satisfaction_comparison:
                if 2 in satisfaction_comparison:
                    continue  # objects are incomparable, skip
                else:
                    continue  # obj1 is preferred over obj2, skip
            elif 2 in satisfaction_comparison:
                if 1 in satisfaction_comparison:
                    continue  # objects are incomparable, skip
                else:
                    is_optimal = False  # obj1 is not optimal, return false and break
                    break
            else:
                continue  # objs are equal, skip
        return is_optimal

    def is_optimal_penalty_object(self, obj1):
        """
        Checks if the feasible object meets the criteria for an optimal object
        according to the penalty logic rules of the problem.

        :param obj1 (Object): The feasible object in consideration.
        :return (Boolean): True if optimal, False otherwise.
        """
        is_optimal = True
        for obj2 in self.feasible_objects:
            if obj1.get_total_penalty() == obj2.get_total_penalty():  # objs are equal, skip
                continue
            elif obj1.get_total_penalty() < obj2.get_total_penalty():  # obj1 is strictly preferred, skip
                continue
            else:  # obj1 is not optimal, set is_optimal to False and break out of loop
                is_optimal = False
                break
        return is_optimal
