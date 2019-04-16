"""
My Utilities, author = jbr185, 66360439

Just some helpful functions for my python coding
"""
from sys import argv, exit

def getCommandLineArgument(index, dataType=str, bounded=False, lower=0, upper=0, correction=True):
    """
    This function gets the commandline argument of the given index, then changes it to the data type
    if given. The returned value can be bounded between an upper and lower value if stated and dataType 
    is a number (int or float) and the value lies outside the given range the the user will be prompted 
    to replace it, if correction is set to True or omitted
    """
    try:
        value = dataType(argv[index + 1]) #try to convert the argument to the given dataType
        while dataType in [int, float] and bounded and (value < lower or value > upper):
            print("Argument", index, "is invaild, Please type a number between", lower, "and", upper)
            if not correction: #if correction is False, exit
                pause()
                exit()            
            try:
                return dataType(input("> ")) #try to convert the corrected value
            except ValueError:
                continue
        return value
    except ValueError: #if value is not of type given
        return False
    except IndexError: #if argument is not present
        return False    
    
def getInput(prompt="", dataType=str, bounded=False, lower=0, upper=0):
    """
    Prompts the user for an input, a prompt can be given along with a dataType to convert to. if the value
    cannot be converted to the given type then the user will be prompted to input a new value. If the data
    type is a number (float or int) then the value can be bounded to a given upper and lower limit
    """
    print(prompt)
    result = input("> ")
    while True:
        try:
            result = dataType(result) #try to convert to data type given
            if (dataType in [int, float] and bounded and (result < lower or result > upper)):
                print("Please type a number between", lower, "and", upper)
                result = input("> ")
            else:
                return result
        except ValueError: #if the input cannot be converted to the datatype, prompt the user to retry
            print("Invalid Input!")
            result = input("> ")
            
def pause(prompt="Press Enter to Continue..."):
    """
    Pauses the console until the user presses the Enter key. A custom prompt can be given
    """
    return input(prompt)