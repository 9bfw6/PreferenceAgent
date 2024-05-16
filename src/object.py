class Object:
    """
    This class represents an object in the preference problem.

    Attributes:
    - name (str): The name of the object.
    - encoding (str): The binary encoding of the object.
    - values (list): An arrangement of attributes associated with each object.
    - integers (list): An integer representation of the values of the object.
    - total_penalty (int): The total penalty logic penalty associated with this object.
    """
    def __init__(self, name, encoding, values, integers):
        """
        Initializes a new Object.

        :param name (str): The name of the object.
        :param encoding (str): The binary encoding of the object.
        :param values (list): An arrangement of attributes associated with each object.
        :param integers (list): An integer representation of the values of the object.
        """
        self.name = name
        self.encoding = encoding
        self.values = values
        self.integers = integers
        self.total_penalty = 0

    def __str__(self):
        """
        Prints the values of the objects as a string.

        :return: None.
        """
        output_string = ", ".join(self.values)
        print(self.name + f" - {output_string}")

    def return_integer_values(self):
        """
        Returns the list of integer values associated with this object.

        :return (list): integers.
        """
        return self.integers

    def return_test_integers(self):
        """
        Returns the object's list of integers in a format such that the object can
        be used in pysat.

        :return (list): test_list
        """
        test_list = []
        for integer in self.integers:
            test_int = [integer]
            test_list.append(test_int)
        return test_list

    def add_penalty(self, penalty):
        """
        Adds a penalty associated with penalty logic to this object's total penalty.

        :param penalty (int): the penalty to be added to this object's total penalty.
        :return: None.
        """
        self.total_penalty += int(penalty)

    def get_total_penalty(self):
        """
        Returns this object's total penalty to caller.
        :return (int): total_penalty
        """
        return self.total_penalty

    def get_name(self):
        """
        Returns the name of this object to the caller.
        :return (str): name
        """
        return self.name
