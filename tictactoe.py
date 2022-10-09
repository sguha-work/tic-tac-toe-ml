import calendar
import time
import json


class TicTacToe:
    # this variable will hold the present game file name
    __game_file_name = ''
    # this variable is the file pointer
    __game_file_pointer = None
    __valid_moves = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
    __occupied_coordinates = []

    number_of_steps = 6

    def __int__(self):
        current_gmt = time.gmtime()
        time_stamp = calendar.timegm(current_gmt)
        self.__game_file_name = 'game/' + str(time_stamp)

    def __log_move_to_game_file(self):
        self.__game_file_pointer = open(self.__game_file_name, "a")
        self.__game_file_pointer.write(json.dump(self.__occupied_coordinates))
        self.__game_file_pointer.close()

    def check_user_input(self, user_input):
        if user_input in self.__valid_moves:
            return True
        else:
            return False

    def input(self, step, move_coordinates):
        print(f"step number {step}! user input coordinate {move_coordinates}")
        self.__occupied_coordinates.append(move_coordinates)
        self.__log_move_to_game_file()

    def get_move(self):
        return '00'
