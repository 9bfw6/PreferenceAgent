Program Name: Preference Agent
Author: Brooks Forrest Woelfel


src directory files:
main.py
datahandler.py 
object.py
penaltylogic.py
qualitativechoicelogic.py
preferenceproblem.py



ExampleTestCase directory files:
attributes.txt
constraints.txt
penaltylogic.txt
qualitativechoicelogic.txt



TestCase directory files:
attributes.txt
constraints.txt
penaltylogic.txt
qualitativechoicelogic.txt



Driver file: 
main.py



Packages installed:
pySAT
prettytable



To run this program:

Before you can run my program, make sure that pySAT and prettytable are both installed. 
This can be done with the following commands:
pip install python-sat[pblib,aiger]
pip install prettytable


Next, open a new terminal shell and navigate to the directory of this project folder, 
then type python followed by src/main.py. The program will prompt you to first enter the
testing directory of choice, followed by the file names of that directory to be tested.

For instance, if you wish to use the TestCase directory, the program input should be:

Enter the testing directory for this problem: TestCase
Enter Attributes File Name: attributes.txt
Enter Hard Constraints File Name: constraints.txt
Enter Penalty Logic File Name: penaltylogic.txt
Enter Qualitative Choice Logic File Name: qualitativechoicelogic.txt


