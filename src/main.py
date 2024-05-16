from datahandler import DataHandler
from preferenceproblem import PreferenceProblem

"""
The driver module of the program. This module manages the user interface, collects
the file names from the user, and instantiates DataHandler and PreferenceProblem 
objects which are used to process the file data and solve the preference problem.
"""


def display_menu(preference_problem):
    """
    Displays the main menu to the user.

    :param preference_problem (PreferenceProblem): The preference problem.
    :return: None.
    """
    flag = True
    while flag:
        print_home_screen()
        choice = input("Your Choice: ")
        match choice:
            case '1':
                penalty_logic_menu(preference_problem)
            case '2':
                qualitative_choice_logic_menu(preference_problem)
            case '3':
                flag = False
                print("Bye!")
            case _:
                print("Invalid Choice! Please try again.")


def penalty_logic_menu(preference_problem):
    """
    Displays the penalty logic menu to the user.

    :param preference_problem (PreferenceProblem): The preference problem.
    :return: None.
    """
    flag = True
    while flag:
        print_preference_options()
        choice = input("Your Choice: ")
        match choice:
            case '1':
                preference_problem.encoding()
            case '2':
                preference_problem.return_feasibility()
            case '3':
                preference_problem.print_penalty_table()
            case '4':
                preference_problem.penalty_exemplification()
            case '5':
                preference_problem.penalty_omni_optimization()
            case '6':
                flag = False
            case _:
                print("Invalid Choice! Please try again.")


def qualitative_choice_logic_menu(preference_problem):
    """
    Displays the qualitative choice logic menu to the user.

    :param preference_problem (PreferenceProblem): the preference problem.
    :return: None.
    """
    flag = True
    while flag:
        print_preference_options()
        choice = input("Your Choice: ")
        match choice:
            case '1':
                preference_problem.encoding()
            case '2':
                preference_problem.return_feasibility()
            case '3':
                preference_problem.print_qualitative_table()
            case '4':
                pass
                preference_problem.qualitative_exemplification()
            case '5':
                preference_problem.qualitative_omni_optimization()
            case '6':
                flag = False
            case _:
                print("Invalid Choice! Please try again.")


def new_preference_problem():
    """
    Collects the necessary files from the user, instantiates DataHandler and
    PreferenceProblem objects, and returns the PreferenceProblem object to main.

    :return (PreferenceProblem): new_problem
    """
    print("Welcome to PrefAgent!\n")
    directory = input("Enter the testing directory for this problem: ")
    attributes_file = input("Enter Attributes File Name: ")
    constraints_file = input("Enter Hard Constraints File Name: ")
    penalty_file = input("Enter Penalty Logic File Name: ")
    qualitative_choice_file = input("Enter Qualitative Choice Logic File Name: ")
    handler = DataHandler()
    handler.read_attributes(f"{directory}/{attributes_file}")
    constraints = handler.read_constraints(f"{directory}/{constraints_file}")
    objects = handler.make_objects()
    penalty_logics = handler.read_penalty_logic(f"{directory}/{penalty_file}")
    qualitative_logics = handler.read_qualitative_logic(f"{directory}/{qualitative_choice_file}")
    new_problem = PreferenceProblem(objects, constraints, penalty_logics, qualitative_logics)
    return new_problem


def print_home_screen():
    """
    Prints the home screen.

    :return: None.
    """
    print("Choose the preference logic to use:")
    print("1. Penalty Logic")
    print("2. Qualitative Choice Logic")
    print("3. Exit")


def print_preference_options():
    """
    Prints the preference logic options.

    :return: None.
    """
    print("Choose the reasoning task to perform:")
    print("1. Encoding")
    print("2. Feasibility Checking")
    print("3. Show the Table")
    print("4. Exemplification")
    print("5. Omni-optimization")
    print("6. Back to previous menu")


def main():
    """
    The main method.

    :return: None.
    """
    preference_problem = new_preference_problem()
    display_menu(preference_problem)


if __name__ == "__main__":
    main()
