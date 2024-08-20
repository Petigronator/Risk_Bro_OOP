#GUI_Workflow.py

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from SM_InputValidator import SM_InputValidator
from SM_StdCalculator import SM_StdCalculator
from SM_VarCalculator import SM_VarCalculator
from SM_GraphDisplay import SM_GraphDisplay
from telegram import Bot
import os


class SM_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.validator = SM_InputValidator()
        self.init_ui()
        # Load Telegram Bot token from environment variables
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if self.telegram_bot_token:
            self.telegram_bot = Bot(token=self.telegram_bot_token)
        else:
            print("Telegram bot token not found.")
            self.telegram_bot = None
        
    def init_ui(self):
        self.setWindowTitle("Risk Bro")
        self.setGeometry(300, 300, 500, 350)  # Adjusted for a larger window
    
    # Apply futuristic CSS styles with updated button styles
        self.setStyleSheet("""
    QWidget {
        font-size: 16px;
        color: #FFFFFF;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1A1A1D, stop:1 #131313);
        font-family: 'Roboto', sans-serif;
    }
    QLabel {
        font-weight: bold;
        margin-bottom: 5px;
        font-size: 14px;
        color: #FFFFFF;
    }
    QLineEdit {
        border: 2px solid #00FFFF;
        border-radius: 15px;
        padding: 15px;
        background-color: #2C2C2E;
        color: #FFFFFF;
        margin-bottom: 15px;
        font-size: 14px;
    }
    QPushButton {
        border: 1px solid #8A2BE2;
        border-radius: 15px;
        padding: 15px;
        color: #FFFFFF;
        font-weight: bold;
        margin-bottom: 15px;
        font-size: 14px;
        text-transform: uppercase;
        background: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #007FFF, stop:1 #00FFFF);

    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0.5, x2:1, y2:0.5, stop:0 #007FFF, stop:1 #00FFFF);

    }
    QPushButton:pressed {
        background-color: #C471ED;
    }
    """)


        self.layout = QVBoxLayout()
        
        # Security Ticker Label and Input
        self.security_symbol_label = QLabel("Security Ticker:")
        self.layout.addWidget(self.security_symbol_label)
        self.security_symbol_input = QLineEdit(self)
        self.security_symbol_input.setPlaceholderText("Enter a security ticker (e.g., AAPL)")
        self.layout.addWidget(self.security_symbol_input)
        
        # Start Date Label and Input
        self.start_date_label = QLabel("Start Date:")
        self.layout.addWidget(self.start_date_label)
        self.start_date_input = QLineEdit(self)
        self.start_date_input.setPlaceholderText("Enter start date (YYYY-MM-DD)")
        self.layout.addWidget(self.start_date_input)
        
        # End Date Label and Input
        self.end_date_label = QLabel("End Date:")
        self.layout.addWidget(self.end_date_label)
        self.end_date_input = QLineEdit(self)
        self.end_date_input.setPlaceholderText("Enter end date (YYYY-MM-DD)")
        self.layout.addWidget(self.end_date_input)
        
        # Telegram ID Label and Input
        self.telegram_chat_id_label = QLabel("Telegram Chat ID:")
        self.layout.addWidget(self.telegram_chat_id_label)
        self.telegram_chat_id_input = QLineEdit(self)
        self.telegram_chat_id_input.setPlaceholderText("Enter Telegram chat ID")
        self.layout.addWidget(self.telegram_chat_id_input)
        
        # Buttons
        self.STD_Calculation_button = QPushButton("Calculate Standard Deviation", self)
        self.STD_Calculation_button.clicked.connect(self.on_STD_calculate_clicked)
        self.layout.addWidget(self.STD_Calculation_button)
        
        self.Variance_Calculation_Button = QPushButton("Calculate Variance", self)
        self.Variance_Calculation_Button.clicked.connect(self.on_VAR_calculate_clicked)
        self.layout.addWidget(self.Variance_Calculation_Button)
        
        self.Graph_Display_Button = QPushButton("Display Adjusted Close Graph", self)
        self.Graph_Display_Button.clicked.connect(self.on_Graph_Display_clicked)
        self.layout.addWidget(self.Graph_Display_Button)
        
        self.setLayout(self.layout)
        
    def send_telegram_message(self, chat_id, message, image_path=None):
            if not self.telegram_bot or not chat_id:
                return

            try:
                if image_path:
                    with open(image_path, 'rb') as image_file:
                        self.telegram_bot.send_photo(chat_id=chat_id, photo=image_file, caption=message)
                else:
                    self.telegram_bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                QMessageBox.warning(f"Failed to send Telegram message: {e}")
            
    def check_empty_inputs(self):
        # Check if any of the key arguments are empty
        if not self.security_symbol_input.text() or not self.start_date_input.text() or not self.end_date_input.text():
            QMessageBox.warning(self, "Missing Arguments", "Please provide all necessary input values.")
            return True
        return False

    def on_STD_calculate_clicked(self):
        #No key inputs exception handling
        if self.check_empty_inputs():
            return

        else:
            security_symbol = self.security_symbol_input.text().upper()
            start_date = self.start_date_input.text()
            end_date = self.end_date_input.text()
            Telegram_ID = self.telegram_chat_id_input.text()
        
            #Input Validation Handling
            if not self.validator.Validate_security_symbol(security_symbol) or not self.validator.Validate_start_date(start_date) or not self.validator.Validate_end_date(end_date):
                QMessageBox.warning(self, "Input Validation Failed", "Please enter valid inputs.")
                return
        
            #Date Order exception handling
            if not self.validator.Validate_date_order(start_date,end_date):
                QMessageBox.warning(self, "Date order exception ", "Start date cannot be after end date, Please enter the dates according to the labels")
                return
        
            STD_Calculator = SM_StdCalculator(security_symbol, start_date, end_date)
            std_dev = STD_Calculator.calculate_std(security_symbol, start_date, end_date)
            QMessageBox.information(self, "Calculation Result", f"The standard deviation of {security_symbol} from {start_date} to {end_date} is: {std_dev}")
        
            #Sending the result as a message if a valid phone number is provided
            if self.validator.Validate_telegram_chat_id(Telegram_ID) and self.telegram_bot:
                message = f"The standard deviation of {security_symbol} from {start_date} to {end_date} is: {std_dev}"
                self.send_telegram_message(message, Telegram_ID)


    def on_VAR_calculate_clicked(self):
        #No key inputs exception handling
        if self.check_empty_inputs():
            return
        else:
            security_symbol = self.security_symbol_input.text().upper()
            start_date = self.start_date_input.text()
            end_date = self.end_date_input.text()
            Telegram_ID = self.telegram_chat_id_input.text()
        
            #Input Validation Handling
            if not self.validator.Validate_security_symbol(security_symbol) or not self.validator.Validate_start_date(start_date) or not self.validator.Validate_end_date(end_date):
                QMessageBox.warning(self, "Input Validation Failed", "Please enter valid inputs.")
                return
        
            #Date Order exception handling
            if not self.validator.Validate_date_order(start_date,end_date):
                QMessageBox.warning(self, "Date order exception ", "Start date cannot be after end date, Please enter the dates according to the labels")
                return
        
            Var_calculator = SM_VarCalculator(security_symbol, start_date, end_date)
            variance = Var_calculator.calculate_var(security_symbol, start_date, end_date)
            QMessageBox.information(self, "Calculation Result", f"The variance of {security_symbol} from {start_date} to {end_date} is: {variance}")
        
            #Sending the result as a message if a valid phone number is provided
            if self.validator.Validate_telegram_chat_id(Telegram_ID) and self.telegram_bot:
                message = f"The variance of {security_symbol} from {start_date} to {end_date} is: {variance}"
                self.send_telegram_message(message, Telegram_ID)

    def on_Graph_Display_clicked(self):
        #No key inputs exception handling
        if self.check_empty_inputs():
            return
        
        else:
            security_symbol = self.security_symbol_input.text().upper()
            start_date = self.start_date_input.text()
            end_date = self.end_date_input.text()
            Telegram_ID = self.telegram_chat_id_input.text()
            
            #Input Validation Handling
            if not self.validator.Validate_security_symbol(security_symbol) or not self.validator.Validate_start_date(start_date) or not self.validator.Validate_end_date(end_date):
                QMessageBox.warning(self, "Input Validation Failed", "Please enter valid inputs.")
                return
            
            #Date Order exception handling
            if not self.validator.Validate_date_order(start_date, end_date):
                QMessageBox.warning(self, "Date order exception", "Start date cannot be after end date. Please enter the dates according to the labels.")
                return

            graph_display = SM_GraphDisplay(security_symbol, start_date, end_date, save_path='Graph_Photo_Generator/Graph.png')
            graph_path = graph_display.plot_adjusted_close()

            # Display the graph to the user regardless of the phone number input
            QMessageBox.information(self, "Graph Display", "The adjusted close price graph has been generated.")

            # Send the graph via WhatsApp if a valid phone number is provided
            if self.validator.Validate_telegram_chat_id(Telegram_ID) and self.telegram_bot:
                self.send_telegram_message("Here's the graph displaying adjusted close prices:", Telegram_ID, image_path= graph_path)
