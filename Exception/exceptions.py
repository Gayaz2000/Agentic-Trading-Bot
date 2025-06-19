import sys
import os

class TradingBotException(Exception):
    def __init__(self, error_messages, error_details:sys):
        self.error_messages = error_messages
        _, _,exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"\nError occured in python script name -> {self.filename},\nLine number -> {self.lineno},\nError messages -> {self.error_messages}"
    

# if __name__ == "__main__":
#     try:
#         a = 1/0
#         print("This will not be printed")
#     except Exception as e:
#         raise TradingBotException(e, sys)