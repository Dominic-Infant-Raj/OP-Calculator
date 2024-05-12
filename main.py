"""
A OP Calculator for students


Author :  Dominic Infant Raj
Date : 11-5-2024

Version : 1
"""

# imports
from math import sqrt
from customtkinter import set_default_color_theme, set_appearance_mode
from customtkinter import CTk, CTkButton, CTkEntry, CTkFrame, CTkLabel
from customtkinter import CTkScrollableFrame, CTkTextbox


# function for setting the theme and default colour of wigets
def set_theme(theme, colour_theme):
    """sets the theme and the colour used on widgets

    Args:
        theme (str): this str sets the theme of the program
                    available options : (System/Dark/Light)
        colour (_type_): _description_
    """
    set_appearance_mode(str(theme))
    set_default_color_theme(str(colour_theme))


class History(CTkScrollableFrame):
    """updates the history of calculations of that session

    Default Args (no need to do anything):
        CTkScrollableFrame (class): Default class for creating a frame with a scrollbar
    Args for this class :
        root (object) : pass the window or the frame you need this calculator frame to be in
        coords (list): Enter the following in the exact order given below:
            1. relx
            2. rely
            3.relheight
            4.relwidth
            so it would look something like this [relx,rely,relheight,relwidth]
            (instead of relx,rely... enter your values)
    """

    def __init__(self, root, coords):
        """Constructor for class history"""
        super().__init__(master=root)
        self.place(
            relx=coords[0], rely=coords[1], relheight=coords[2], relwidth=coords[3]
        )
        CTkLabel(master = self, text="History").pack()

    def update(self, update_string):
        """_summary_

        Args:
            update_string (_type_): _description_
        """
        label = CTkLabel(master=self, text=update_string)
        label.pack()
        return


class Calculator(CTkFrame):
    """Creates a frame with a functional calculator

    Default Args (No need do anything):
        CTkFrame (Class): The default class for creating a frame in customtkinter
    Args for this class :
        root (object) : pass the window or the frame you need this calculator frame to be in
        coords (list): Enter the following in the exact order given below:
            1. relx
            2. rely
            3.relheight
            4.relwidth
            so it would look something like this [relx,rely,relheight,relwidth]
            (instead of relx,rely... enter your values)
        history (object): the history object to update all the succesfull calculations
    """

    expression_str = ""  # the string which holds the exprestion to be calculated

    # Constructor for the Calculator class
    def __init__(self, root, coords, history):
        """Constructor for class Calculator"""
        super().__init__(master=root)
        self.history = history
        self.place(
            relx=coords[0], rely=coords[1], relheight=coords[2], relwidth=coords[3]
        )
        self.set_calc_screen()  # moving to creating the screen of the calculator

    def set_calc_screen(self):
        """Creates the calculator Screen"""
        calc_screen = CTkEntry(master=self)
        calc_screen.place(relx=0.05, rely=0.02, relheight=0.1, relwidth=0.9)
        self.place_button()  # moving to render the buttons in their respective places

    def place_button(self):
        """Places the buttons in the right order"""
        # creating a frame to hold the numpad
        numpad_frame = CTkFrame(master=self)
        numpad_frame.place(relx=0.05, rely=0.2, relheight=0.75, relwidth=0.9)
        # The below lists contains all the characters displayed on the button on the numpad
        numpad_row_1_chars_list = ["√", "π", "^", "x²"]
        numpad_row_2_chars_list = ["÷", "×", "-", "+"]
        numpad_row_3_chars_list = ["(", "7", "8", "9"]
        numpad_row_4_chars_list = [")", "4", "5", "6"]
        numpad_row_5_chars_list = [".", "1", "2", "3"]
        numpad_row_6_chars_list = ["C", "⌫", "0", "="]
        list_of_numpad_chars_lists = [
            numpad_row_1_chars_list,
            numpad_row_2_chars_list,
            numpad_row_3_chars_list,
            numpad_row_4_chars_list,
            numpad_row_5_chars_list,
            numpad_row_6_chars_list,
        ]

        # loops through all the characters and displays them in Buttons in the Numpad
        button_width = 0.2
        button_height = 0.1

        # Calculate the total number rows
        total_rows = len(list_of_numpad_chars_lists)

        # Calculate the horizontal and vertical gap between buttons
        horizontal_gap = (1 - button_width * len(numpad_row_1_chars_list)) / (
            len(numpad_row_1_chars_list) + 1
        )
        vertical_gap = (1 - button_height * total_rows) / (total_rows + 1)

        # Loop through each row and button
        for row_index, row_chars_list in enumerate(list_of_numpad_chars_lists):
            for col_index, char in enumerate(row_chars_list):
                # Calculate the position of the button
                x_pos = (col_index + 1) * horizontal_gap + col_index * button_width
                y_pos = (row_index + 1) * vertical_gap + row_index * button_height

                button = CTkButton(
                    master=numpad_frame,
                    text=char,
                    command=lambda val=char: self.update_calc_screen(string=val),
                )
                button.place(
                    relx=x_pos,
                    rely=y_pos,
                    relwidth=button_width,
                    relheight=button_height,
                )

    def update_calc_screen(self, string):
        """Updates the Expression shown in the calculator screen"""
        calc_screen = self.winfo_children()[0]  # Accessing the calculator screen widget

        if string == "⌫" and len(calc_screen.get()) != 0:
            calc_screen.delete(len(calc_screen.get()) - 1, "end")
        elif string == "C":
            calc_screen.delete(0, "end")
        elif string == "=":
            result = self.evaluate_expression(expression=calc_screen.get())
            calc_screen.delete(0, "end")  # Clear the calculator screen
            calc_screen.insert("end", result)  # Display the result
        elif string == "x²":
            calc_screen.insert("end", "²")
        else:
            calc_screen.insert("end", string)

    def evaluate_expression(self, expression):
        """Calculates the answer from the expression"""

        # replacing math operators which have alternative python operators
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")

        # variables required in this module
        expression_in_list = list(expression)
        valid_python_expression_list = []
        valid_python_expression = ""
        original_math_expression = expression
        basic_operators = ["+", "-", "*", "/"]

        
        # converting the mathematical expression to a python expression
        for e in expression_in_list:
            index_e = expression_in_list.index(e)
            if e == "²":
                if (len(expression_in_list) - 1) == index_e:
                    valid_python_expression_list.append("**2")
                elif expression_in_list[(index_e + 1)] in basic_operators:
                    valid_python_expression_list.append("**2")
                else:
                    valid_python_expression_list.append("**2*")

            elif e == "(":
                if expression_in_list.index(e) == 0:
                    valid_python_expression_list.append("(")
                elif expression_in_list[(index_e - 1)] not in basic_operators:
                    valid_python_expression_list.append("*(")
                else:
                    valid_python_expression_list.append("(")

            elif e == ")":
                if index_e == (len(expression_in_list) - 1):
                    valid_python_expression_list.append(")")
                elif expression_in_list[(index_e + 1)] not in basic_operators:
                    valid_python_expression_list.append(")*")
                else:
                    valid_python_expression_list.append(")")

            elif e == "π":
                if index_e == 0:
                    valid_python_expression_list.append("22/7")
                elif index_e == (len(expression_in_list) - 1):
                    valid_python_expression_list.append("*22/7")
                elif (
                    expression_in_list[(index_e + 1)] not in basic_operators
                    and expression_in_list[(index_e - 1)] not in basic_operators
                ):
                    valid_python_expression_list.append("*22/7*")
                elif expression_in_list[(index_e + 1)] not in basic_operators:
                    valid_python_expression_list.append("22/7*")
                elif expression_in_list[(index_e - 1)] not in basic_operators:
                    valid_python_expression_list.append("*22/7")
                else:
                    valid_python_expression_list.append("22/7")

            elif e == "√":

                def do_root():
                    str_of_digits_after_root = ""
                    x = 0  # Used in the below while loop
                    while True:
                        x += 1
                        # Checking if assigning a char var will result in an error as index is out of range
                        if (index_e + x) >= len(expression_in_list):
                            break
                        else:
                            char = expression_in_list[index_e + x]
                        # Checking if the char is a part of the number to be rooted
                        if char in basic_operators:
                            break
                        else:
                            str_of_digits_after_root += char
                            print(expression_in_list)
                            print(char)
                            expression_in_list.remove(char)

                        if str_of_digits_after_root:
                            root_ans = sqrt(
                                float(str_of_digits_after_root)
                            )  # Getting the root of the number
                            return root_ans
                        else:
                            # Handle the case when there are no digits after the square root symbol
                            raise ValueError(
                                "Invalid expression: No digits found after square root symbol"
                            )

                if index_e == 0:
                    valid_python_expression_list.append(f"{do_root()}")
                elif expression_in_list[(index_e - 1)] not in basic_operators:
                    valid_python_expression_list.append(f"*{do_root()}")
                else:
                    valid_python_expression_list.append(f"{do_root()}")

            else:
                valid_python_expression_list.append(e)

        print(valid_python_expression_list)
        for i in valid_python_expression_list:
            valid_python_expression += i

        ans = eval(valid_python_expression)
        self.history.update(f"_________________\n{original_math_expression}\n={ans}\n________________")
        return ans

class Textbox(CTkTextbox):
    """A textbox for students to write anything they want

    Args:
        CTkTextbox (class): Default class for Making  textbox
    """
    def __init__(self,root,coords):
        super().__init__(master=root)
        self.place(
            relx=coords[0], rely=coords[1], relheight=coords[2], relwidth=coords[3]
        )
        self.insert("0.0","Free Area ... u can type anything here... :)")

# Rendering everything to the screen
win = CTk()
win.title("OG_CALCULATOR")
win.geometry("1200x600")
set_theme(theme="System", colour_theme="blue")
history = History(root=win, coords=[0.03, 0.05, 0.9, 0.2])
Calculator(root=win, coords=([0.25, 0.05, 0.9, 0.32]), history=history)
Textbox(root=win,coords=[0.60, 0.05, 0.9, 0.37])
win.mainloop()
