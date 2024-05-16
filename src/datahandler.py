from object import Object
from penaltylogic import PenaltyLogic
from qualitativechoicelogic import QualitativeChoiceLogic
import re


class DataHandler:
    """
    This class organizes several methods for reading in data from files and processing it.

    Attributes:
    - attributes (list): A list containing the values of each attribute of the problem.
    - values (dict): A dictionary that maps each attribute value to a binary value, 1 or 0.
    - objects (list): A list of Object instances.
    - constraints (list): A list of containing the hard constraints of the problem.
    - penalty_objects (list): A list containing PenaltyLogic instances.
    - qualitative_objects (list): A list containing QualitativeChoiceLogic instances.
    """
    def __init__(self):
        """
        Initializes the DataHandler object.

        """
        self.attributes = []  # list containing each boolean value of the attribute boolean variable
        self.values = {}  # hash table matching each boolean value with a binary code
        self.objects = []  # list of Object objects
        self.constraints = []
        self.penalty_objects = []
        self.qualitative_objects = []

    def read_attributes(self, filepath):
        """
        Reads the attributes file line by line and processes its data.

        :param filepath (str): The filepath.
        :return: None.
        """
        with open(filepath, "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            for line in lines:
                current_line = line.split(": ")
                category = current_line[0]
                values = current_line[1].split(", ")
                self.values[values[0]] = 1
                self.values[values[1]] = 0
                self.attributes.append(values)

    def read_constraints(self, filepath):
        """
        Reads the constraints file line by line and processes its data, and returns
        the data as a list to the caller.

        :param filepath (str): The filepath.
        :return (list): constraints
        """
        with open(filepath, "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            for line in lines:
                clause_list = self.make_constraints(line)
                for clause in clause_list:
                    self.constraints.append(clause)
            self.add_base_constraints()
            return self.constraints

    def read_penalty_logic(self, filepath):
        """
        Reads the penalty logic file line by line and processes its data, and returns the
        data as a list to the caller.

        :param filepath (str): The filepath.
        :return (list): penalty_objects
        """
        with open(filepath, "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            for line in lines:
                line_elements = line.split(", ")
                cnf_formula = line_elements[0]
                penalty_value = line_elements[1]
                cnf_constraints = self.make_constraints(cnf_formula)
                penalty_logic = PenaltyLogic(cnf_formula, cnf_constraints, penalty_value)
                self.penalty_objects.append(penalty_logic)
        return self.penalty_objects

    def read_qualitative_logic(self, filepath):
        """
        Reads the qualitative logic file line by line and processes its data, and returns
        the data as a list to the caller.

        :param filepath (str): The filepath.
        :return (list): qualitative_objects
        """
        with open(filepath, "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            for line in lines:
                values = re.split(' IF | IF', line)
                constraints = []
                logic = values[0]
                condition = values[1]
                if condition == '':
                    values.pop(1)
                condition_constraint = None
                if len(values) == 2:
                    condition = values[1]
                    condition_constraint = self.make_constraints(condition)
                clauses = logic.split(" BT ")
                for clause in clauses:
                    clause_list = self.make_constraints(clause)
                    constraints.append(clause_list)
                qualitative_logic = QualitativeChoiceLogic(line, constraints, condition_constraint)
                self.qualitative_objects.append(qualitative_logic)
        return self.qualitative_objects

    def make_objects(self):
        """
        From the list of attributes in the class, creates and instantiates new Objects
        and stores them in a list. Each object has a unique binary encoding.

        :return (list): The list of objects.
        """
        integer_value = 0
        num_of_bits = len(self.attributes)
        num_of_sets = 2 ** num_of_bits
        while integer_value < num_of_sets:
            object_number = integer_value
            object_name = f"o{object_number}"
            object_values = []
            object_integers = []
            encoded_string = self.encode_string(integer_value, num_of_bits)
            integer = 1
            for index, item in enumerate(encoded_string):
                object_integer = integer
                attribute_variable = self.attributes[index]
                bit_value = int(item)
                if bit_value == 0:
                    target_index = 1
                    object_integer = -integer
                else:
                    target_index = 0
                attribute_value = attribute_variable[target_index]
                object_values.append(attribute_value)
                object_integers.append(object_integer)
                integer += 1
            new_object = Object(object_name, encoded_string, object_values, object_integers)
            self.objects.append(new_object)
            integer_value += 1
        return self.objects

    def make_constraints(self, line):
        """
        Given a string representing a logic formula, formats it such that it can be used
        by pysat.

        :param line (str): A string of code representing a logic formula.
        :return (list): A list holding the formula.
        """
        clause = []
        clause_list = []
        clauses = line.split(" AND ")
        for a_clause in clauses:
            clause.clear()
            literals = a_clause.split(" OR ")
            if len(literals) == 1:
                for literal in literals:
                    attribute_value = literal.split(" ")
                    if len(attribute_value) == 2:
                        value = attribute_value[1]
                        integer = self.return_integer(value)
                        bit_value = self.values[value]
                        if bit_value == 1:
                            integer = -integer
                        new_clause = [integer]
                        clause_list.append(new_clause)
                    else:
                        value = attribute_value[0]
                        integer = self.return_integer(value)
                        bit_value = self.values[value]
                        if bit_value == 0:
                            integer = -integer
                        new_clause = [integer]
                        clause_list.append(new_clause)
            else:
                for literal in literals:
                    attribute_value = literal.split(" ")
                    if len(attribute_value) == 2:
                        value = attribute_value[1]
                        integer = self.return_integer(value)
                        bit_value = self.values[value]
                        if bit_value == 1:
                            integer = -integer
                        clause.append(integer)
                    else:
                        value = attribute_value[0]
                        integer = self.return_integer(value)
                        bit_value = self.values[value]
                        if bit_value == 0:
                            integer = -integer
                        clause.append(integer)
            if clause:
                clause_list.append(clause)
        return clause_list

    def encode_string(self, integer_value, num_of_bits):
        """
        Given an integer value, converts it to a binary string representation with a specified
        number of bits.
        :param integer_value (int): The integer to be converted.
        :param num_of_bits (int): The desired number of bits.
        :return (str): The binary string representation of the integer value.
        """
        encoded_string = (format(integer_value, f'0{num_of_bits}b'))
        return encoded_string

    def return_integer(self, value):
        """
        Retrieves the corresponding integer from the attribute value, so that a formula
        can be built and evaluated by pysat.

        :param value (str): The attribute value.
        :return (int): The integer form of the attribute value.
        """
        target_integer = 0
        for index, item in enumerate(self.attributes, 1):
            if value in item:
                target_integer = index
                break
        return target_integer

    def add_base_constraints(self):
        """
        Adds the base constraints to the hard constraints formula, so that

        it can be evaluated by pysat.
        :return: None.
        """
        for index, item in enumerate(self.attributes, 1):
            base_constraint = []
            value1 = -index
            value2 = index
            base_constraint.append(value1)
            base_constraint.append(value2)
            self.constraints.append(base_constraint)
