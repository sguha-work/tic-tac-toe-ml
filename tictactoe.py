import calendar
import time
import json
import itertools
import os


class TicTacToe:
    __brain_file_name = 'brain.json'
    __brain_file_pointer = None
    # this variable will hold the present game file name
    __game_file_name = ''
    # this variable is the file pointer
    __game_file_pointer = None
    # this is the list of valid moves, will be used to check user input
    __valid_moves = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
    # this list will hold the occupied coordinates, first move is always by user
    __occupied_coordinates = []
    # following variable holds the wining coordinates, each of which can be reversed or reorders
    __winning_coordinates = [
        ['00', '01', '02'],
        ['10', '11', '12'],
        ['20', '21', '22'],
        ['00', '10', '20'],
        ['01', '11', '21'],
        ['02', '12', '22'],
        ['00', '11', '22'],
        ['02', '11', '20']
    ]
    number_of_steps = 6

    def __int__(self):
        if not os.path.isdir("games"):
            os.makedirs("games")
        current_gmt = time.gmtime()
        time_stamp = calendar.timegm(current_gmt)
        self.__game_file_name = 'games/' + str(time_stamp) + '.json'
        self.__game_file_pointer = open(self.__game_file_name, "a")
        self.__game_file_pointer.close()
        temp_array = []
        index = 0
        for move in self.__winning_coordinates:
            for x in itertools.permutations(move):
                temp_array.append(list(x))
            index += 1
        self.__winning_coordinates = temp_array

    # this method logs the move(by user or by computer) to game file
    def __log_move_to_game_file(self):
        print(f'file name {self.__game_file_name}')
        self.__game_file_pointer = open(self.__game_file_name, "w")
        self.__game_file_pointer.write(json.dumps(self.__occupied_coordinates))
        self.__game_file_pointer.close()

    def __update_brain_file(self, data_to_write):
        self.__brain_file_pointer = open(self.__brain_file_name, 'r')
        existing_data_in_brain = json.loads(self.__brain_file_pointer.read())
        self.__brain_file_pointer.close()
        for data in data_to_write:
            existing_data_in_brain.append(data)
        self.__brain_file_pointer = open(self.__brain_file_name, 'w')
        self.__brain_file_pointer.write(json.dumps(existing_data_in_brain))

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
        pass

    def user_win(self):
        # filtering user moves from occupied coordinates
        user_moves = []
        permuted_user_moves = []
        for index, move in enumerate(self.__occupied_coordinates):
            if index % 2:
                user_moves.append(move)
        flag = False
        if len(user_moves) == 3:
            for winning_move in self.__winning_coordinates:
                if winning_move[0] == user_moves[0] and winning_move[1] == user_moves[1] and winning_move[2] == \
                        user_moves[2]:
                    flag = True
                    break
        else:
            for user_move in itertools.combinations(user_moves, 3):
                for permuted_move in itertools.permutations(list(user_move)):
                    permuted_user_moves.append(list(permuted_move))

            for permuted_user_move in permuted_user_moves:
                for winning_move in self.__winning_coordinates:
                    if winning_move[0] == permuted_user_move[0] and permuted_user_move[1] == user_moves[1] and \
                            winning_move[2] == permuted_user_move[2]:
                        flag = True
                        break
                if flag is True:
                    break
        # as user wins logging the move to brain for computer
        if flag is True:
            data_to_write = [user_moves]
            if len(permuted_user_moves):
                data_to_write = permuted_user_moves
            self.__update_brain_file(data_to_write)
            pass
        return flag
