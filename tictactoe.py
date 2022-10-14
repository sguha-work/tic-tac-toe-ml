import calendar
import time
import json
import itertools
import os
import random
import numpy


class TicTacToe:
    __first_move_by_computer = True
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
        self.__game_file_pointer = open(self.__game_file_name, "w")
        self.__game_file_pointer.write(json.dumps(self.__occupied_coordinates))
        self.__game_file_pointer.close()

    def __belongs_to_lists(self, list1, list2):
        for data in list1:
            if numpy.array_equal(data, list2):
                return True
        return False

    def __update_brain_file(self):
        self.__brain_file_pointer = open(self.__brain_file_name, 'r')
        existing_data_in_brain = json.loads(self.__brain_file_pointer.read())
        self.__brain_file_pointer.close()
        # preparing permuted data for brain file
        user_moves = self.__occupied_coordinates[0::2]  # getting even position's values
        computer_moves = self.__occupied_coordinates[1::2]  # getting odd position's value
        for user_move in itertools.permutations(user_moves):
            for computer_move in itertools.permutations(computer_moves):
                new_list = []
                loop_length = len(user_move) + len(computer_move)
                user_move_index = 0
                computer_move_index = 0
                for index in range(loop_length):
                    if index % 2 == 0:
                        new_list.append(user_move[user_move_index])
                        user_move_index += 1
                    else:
                        new_list.append(computer_move[computer_move_index])
                        computer_move_index += 1
                if self.__belongs_to_lists(existing_data_in_brain, new_list) is False:
                    existing_data_in_brain.append(new_list)

        self.__brain_file_pointer = open(self.__brain_file_name, 'w')
        self.__brain_file_pointer.write(json.dumps(existing_data_in_brain))
        self.__brain_file_pointer.close()

    def __check_list_equality(self, list1, list2, length):
        flag = True
        for index in range(length):
            if list1[index] != list2[index]:
                flag = False
                break
        return flag

    def __is_user_can_win_on_next_move(self):
        user_moves = self.__occupied_coordinates[0::2]
        return_value = False
        for winning_moves in self.__winning_coordinates:
            if numpy.array_equal(winning_moves, user_moves):
                return_value = winning_moves[2]
                break
        return return_value

    # This method checcks if computer can win on its next move or not, if yes then returns the winning move
    # or else returns False
    def __get_winning_move(self):
        return False

    def __get_random_unoccupied_coordinate(self):
        unoccupied_coordinates = list(
            set(self.__valid_moves).symmetric_difference(set(self.__occupied_coordinates)))
        coordinate = random.choice(unoccupied_coordinates)
        return coordinate

    def check_user_input(self, user_input):
        # if user has given a coordinate which is already occupied rejecting it
        if user_input in self.__occupied_coordinates:
            return False
        else:
            if user_input in self.__valid_moves:
                return True
            else:
                return False

    def input(self, move_coordinates):
        self.__occupied_coordinates.append(move_coordinates)
        self.__log_move_to_game_file()

    # This method returns the computer move
    def get_move(self):
        if self.__first_move_by_computer is True:
            # if this is the first move of computer returning random move
            self.__first_move_by_computer = False
            computer_move = self.__get_random_unoccupied_coordinate()
            self.input(computer_move)
            return computer_move
        else:
            if self.__get_winning_move() is False:
                # if user can win on his/her next move then identifying that and make that move as computer's next move
                user_winning_move = self.__is_user_can_win_on_next_move()
                if user_winning_move is False:
                    self.__brain_file_pointer = open(self.__brain_file_name, 'r')
                    data_in_brain = json.loads(self.__brain_file_pointer.read())
                    self.__brain_file_pointer.close()
                    if len(data_in_brain) == 0:
                        # no data exists in brain so selecting move randomly
                        computer_move = self.__get_random_unoccupied_coordinate()
                        self.input(computer_move)
                        return computer_move
                    else:
                        # data exists in brain file checking if relevant data is present or not

                        # Filtering out the user moves from occupied coordinates
                        # even position's data will be of user
                        lost_game_moves = []
                        for data in data_in_brain:
                            check_list_result = self.__check_list_equality(data[0::2],
                                                                           self.__occupied_coordinates[0::2],
                                                                           len(self.__occupied_coordinates[0::2]))
                            if check_list_result is True:
                                lost_game_moves.append(data)
                        print(f'lost game moves {lost_game_moves}')
                        if len(lost_game_moves) != 0:
                            # need to apply intelligence before move
                            vulnerable_coordinates = []
                            for lost_game_move in lost_game_moves:
                                if lost_game_move[len(self.__occupied_coordinates)] in vulnerable_coordinates:
                                    pass
                                else:
                                    vulnerable_coordinates.append(lost_game_move[len(self.__occupied_coordinates)])
                            print(f'vulnerable coordinates {vulnerable_coordinates}')
                            # filtering out safe coordinates by comparing valid moves and vulnerable coordinates
                            safe_coordinates = list(
                                set(self.__valid_moves).symmetric_difference(set(vulnerable_coordinates)))
                            # filtering out occupied coordinates from safe coordinates
                            safe_coordinates = list(
                                set(safe_coordinates).symmetric_difference(set(self.__occupied_coordinates)))
                            print(f'safe coordinates {safe_coordinates}')
                            if len(safe_coordinates) == 1:
                                computer_move = safe_coordinates[0]
                            else:
                                computer_move = random.choice(safe_coordinates)
                            self.input(computer_move)
                            return computer_move
                        else:
                            # no relevant data exists in brain so selecting move randomly
                            computer_move = self.__get_random_unoccupied_coordinate()
                            self.input(computer_move)
                            return computer_move
                else:
                    computer_move = user_winning_move
                    self.input(computer_move)
                    return computer_move
            else:
                # logic to return winning move by computer should go here
                pass

    def computer_win(self):
        computer_moves = []
        permuted_computer_moves = []
        for index, move in enumerate(self.__occupied_coordinates):
            if index % 2 == 1:
                computer_moves.append(move)
        flag = False
        if len(computer_moves) == 3:
            for winning_move in self.__winning_coordinates:
                if winning_move[0] == computer_moves[0] and winning_move[1] == computer_moves[1] and winning_move[2] == \
                        computer_moves[2]:
                    flag = True
                    break
        else:
            for computer_move in itertools.combinations(computer_moves, 3):
                for permuted_move in itertools.permutations(list(computer_move)):
                    permuted_computer_moves.append(list(permuted_move))

            for permuted_computer_move in permuted_computer_moves:
                for winning_move in self.__winning_coordinates:
                    if winning_move[0] == permuted_computer_move[0] and permuted_computer_move[1] == \
                            computer_moves[1] and winning_move[2] == permuted_computer_move[2]:
                        flag = True
                        break
                if flag is True:
                    break
        return flag

    def user_win(self, update_brain_file=True):
        # filtering user moves from occupied coordinates
        user_moves = []
        permuted_user_moves = []
        for index, move in enumerate(self.__occupied_coordinates):
            if index % 2 == 0:
                user_moves.append(move)
        print(f'occupied coordinates {self.__occupied_coordinates} user moves {user_moves}')
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
        if flag is True and update_brain_file is True:
            self.__update_brain_file()

        return flag

    def is_draw(self):
        if self.computer_win() is False and self.user_win(False) is False:
            return True
        else:
            return False
