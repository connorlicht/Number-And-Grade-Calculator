from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from gui import *
import re
import math

class Logic(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.__error = False
        self.__mode_togle = False
        self.__first_input = False
        
        self.button_add.clicked.connect(lambda: self.character())
        self.button_subtract.clicked.connect(lambda: self.character())
        self.button_multiply.clicked.connect(lambda: self.character())
        self.button_modulo.clicked.connect(lambda: self.character())
        self.button_divide.clicked.connect(lambda: self.character())
        self.button_equal.clicked.connect(lambda: self.compute())
        self.button_clear.clicked.connect(lambda: self.clear())
        self.button_period.clicked.connect(lambda: self.character())
        self.button_backspace.clicked.connect(lambda: self.backspace())
        self.button_zero.clicked.connect(lambda: self.character())
        self.button_one.clicked.connect(lambda: self.character())
        self.button_two.clicked.connect(lambda: self.character())
        self.button_three.clicked.connect(lambda: self.character())
        self.button_four.clicked.connect(lambda: self.character())
        self.button_five.clicked.connect(lambda: self.character())
        self.button_six.clicked.connect(lambda: self.character())
        self.button_seven.clicked.connect(lambda: self.character())
        self.button_eight.clicked.connect(lambda: self.character())
        self.button_nine.clicked.connect(lambda: self.character())
        self.button_mode.clicked.connect(lambda: self.toggle_mode())
        self.button_enter.clicked.connect(lambda: self.grade())
        self.button_grade_clear.clicked.connect(lambda: self.grade_clear())

        self.input_points = [self.input_points_1, self.input_points_2, self.input_points_3, self.input_points_4, self.input_points_5]
        self.label = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]
        
        for input_widget in self.input_points + self.label:
            input_widget.hide()
            
        self.label_total_input.hide()
        self.button_enter.hide()
        self.button_curve.hide()
        self.button_grade_clear.hide()

        self.setFixedSize(600, 500)
        
        
    def character(self):
        self.__input_character = ""
        
        if self.__first_input == True:
            self.__first_input = False
            self.label_type.setText("")
        
        if self.__error == True:
            return
        if self.sender().text() == "X":
            self.__input_character = "*"
        else:
            self.__input_character = self.sender().text()
        self.label_type.setText(self.label_type.text() + self.__input_character)
    
    def backspace(self):
        if self.__first_input == True:
            self.__first_input = False
            self.label_type.setText("")
        if self.__error == True:
            self.__error = False
            self.label_type.setText("")
        else:  
            self.label_type.setText(self.label_type.text()[:-1])
    
        
    def clear(self):
        if self.__first_input == True:
            self.__first_input = False
            self.label_type.setText("")
        if self.__error == True:
            self.__error = False
        self.label_type.setText("")

    def compute(self):
        expression_to_split = self.label_type.text()
        
        # [+*/%] matches any of the self.__operators, \d+ matches any number of digits, \d+\.\d+ matches any number of digits followed by a period followed by any number of digits
        # -(?=\d) matches a negative sign followed by a digit
        # | is the or self.__operator
        # so it is self.__operator or number or decimal or negative sign followed by a digit
        expression = re.findall('[+*/%]|\-?\d+\.\d+|\-?\d+|-(?=\d)', expression_to_split)

        # This should return if there is more than one self.__operator in a row
        # Should be able to do 1+-1 or 1--1 or 1*-1 or 1/-1 or 1%-1 based on the previous regex statement

        for i in range(len(expression) - 1):
            if expression[i] in '+-*/%' and expression[i + 1] in '+-*/%':
                self.__error = True
                self.label_type.setText("Error")
                return
            
            try:
                float(expression[i])
                float(expression[i + 1])
            except ValueError:
                continue
            else:
                self.__error = True
                self.label_type.setText("Error")
                return
    
        self.__result = 0
        self.__operator = ""
        for element in expression:
            if element in '+-*/%':
                self.__operator = element
            else:
                if self.__operator == "+":
                    self.__result += float(element)
                elif self.__operator == "-":
                    self.__result -= float(element)
                elif self.__operator == "*":
                    self.__result *= float(element)
                elif self.__operator == "/":
                    try:
                        self.__result /= float(element)
                    except ZeroDivisionError:
                        self.__result = "Error"
                        self.__error = True
                elif self.__operator == "%":
                    self.__result %= float(element)
                elif self.__operator == "":
                    self.__result = float(element)

        self.label_type.setText(f"{self.__result:5.2f}")
        
    def toggle_mode(self):
        if self.__mode_togle == True:
            for input_widget in self.input_points + self.label:
                input_widget.hide()
            self.label_total_input.hide()
            self.button_enter.hide()
            self.button_curve.hide()
            self.button_grade_clear.hide()
            self.setFixedSize(600, 500)
            self.__mode_togle = False
            self.grade_clear()
        else:
            for input_widget in self.input_points + self.label:
                input_widget.show()
            self.label_total_input.show()
            self.button_enter.show()
            self.button_curve.show()
            self.button_grade_clear.show()
            self.setFixedSize(600, 800)
            self.__mode_togle = True
            
    def letter_grade(self, grade):
        if grade >= 97:
            return "A+"
        elif grade >= 93:
            return "A"
        elif grade >= 90:
            return "A-"
        elif grade >= 87:
            return "B+"
        elif grade >= 83:
            return "B"
        elif grade >= 80:
            return "B-"
        elif grade >= 77:
            return "C+"
        elif grade >= 73:
            return "C"
        elif grade >= 70:
            return "C-"
        elif grade >= 67:
            return "D+"
        elif grade >= 63:
            return "D"
        elif grade >= 60:
            return "D-"
        else:
            return "F"
                 
    def grade(self):
        total = 0
        maximum = 0
        return_list = []
        return_index = []
        try:
            for i in range(len(self.input_points)):
                if self.input_points[i].text() != "":
                    if float(self.input_points[i].text()) < 0:
                        return_list.append("Error")
                        return
                    elif self.button_curve.isChecked():
                        return_list.append(self.letter_grade(math.sqrt(float(self.input_points[i].text())) * 10))
                        total += float(self.input_points[i].text())
                        maximum += 100
                        return_index.append(i)
                    else:
                        return_list.append(self.letter_grade(float(self.input_points[i].text())))
                        total += float(self.input_points[i].text())
                        maximum += 100
                        return_index.append(i)

            for i in range(len(return_list)):
                self.label[return_index[i]].setText(return_list[i])
                
            total /= maximum
            total *= 100
            if self.button_curve.isChecked():
                total = math.sqrt(total) * 10
            self.label_total_input.setText(str(f'{total:3.0f}'))
            self.label_6.setText(self.letter_grade(total))           
        except ValueError:
            self.label_total_input.setText("Error")
            return
        except ZeroDivisionError:
            self.label_total_input.setText("Error")
            return
        
    def grade_clear(self):
        self.label_1.setText("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText("")
        self.label_5.setText("")
        self.label_6.setText("")
        self.label_total_input.setText("")
        self.input_points_1.setText("")
        self.input_points_2.setText("")
        self.input_points_3.setText("")
        self.input_points_4.setText("")
        self.input_points_5.setText("")
        self.button_curve.setChecked(False)