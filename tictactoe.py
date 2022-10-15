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
    number_of_steps = 9

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

    def __differentiate(self, list1, list2):
        large_list = None
        small_list = None
        if len(list1) > len(list2):
            large_list = list1
            small_list = list2
        else:
            large_list = list2
            small_list = list1
        return list(set(large_list) - set(small_list))

    # This method checks list2 belongs under list1 or not, list1 is 2d array or list of lists
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
        permuted_user_moves = []
        for permuted_move in itertools.permutations(user_moves):
            permuted_user_moves.append(list(permuted_move))
        return_value = False
        flag = False
        for move in self.__winning_coordinates:
            for user_move in permuted_user_moves:
                if move[0] in user_move and move[1] in user_move:
                    return_value = move[2]
                    flag = True
                    break
            if flag is True:
                break
        if return_value in self.__occupied_coordinates:
            return_value = False
        return return_value

    # This method checcks if computer can win on its next move or not, if yes then returns the winning move
    # or else returns False
    def __get_winning_move(self):
        computer_moves = self.__occupied_coordinates[1::2]
        return_value = False
        for winning_moves in self.__winning_coordinates:
            if numpy.array_equal(winning_moves, computer_moves):
                return_value = winning_moves[2]
                break
        if return_value in self.__occupied_coordinates:
            return_value = False
        return return_value

    def __get_random_unoccupied_coordinate(self):
        unoccupied_coordinates = self.__differentiate(self.__valid_moves, self.__occupied_coordinates)
        coordinate = random.choice(unoccupied_coordinates)
        return coordinate

    def __filter_occupied_coordinates(self, moves):
        filtered_moves = []
        for move in moves:
            if move in self.__occupied_coordinates:
                continue
            else:
                filtered_moves.append(move)
        return filtered_moves

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
        computer_move = ''
        if self.__first_move_by_computer is True:
            # if this is the first move of computer returning random move
            self.__first_move_by_computer = False
            computer_move = self.__get_random_unoccupied_coordinate()
        else:
            computer_winning_move = self.__get_winning_move()
            if computer_winning_move is False:
                # if user can win on his/her next move then identifying that and make that move as computer's next move
                user_winning_move = self.__is_user_can_win_on_next_move()
                print(f'user_winning_move {user_winning_move}')
                if user_winning_move is False:
                    self.__brain_file_pointer = open(self.__brain_file_name, 'r')
                    data_in_brain = json.loads(self.__brain_file_pointer.read())
                    self.__brain_file_pointer.close()
                    if len(data_in_brain) == 0:
                        # no data exists in brain so selecting move randomly
                        computer_move = self.__get_random_unoccupied_coordinate()
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
                            safe_coordinates = self.__differentiate(self.__valid_moves, vulnerable_coordinates)
                            print(f'safe coordinate step 1 {safe_coordinates}')
                            # filtering out occupied coordinates from safe coordinates
                            safe_coordinates = self.__filter_occupied_coordinates(safe_coordinates)
                            print(f'safe coordinates--> {safe_coordinates}')
                            if len(safe_coordinates) == 1:
                                computer_move = safe_coordinates[0]
                            else:
                                computer_move = random.choice(safe_coordinates)
                        else:
                            # no relevant data exists in brain so selecting move randomly
                            computer_move = self.__get_random_unoccupied_coordinate()

                else:
                    computer_move = user_winning_move
            else:
                # logic to return winning move by computer should go here
                computer_move = computer_winning_move
        self.input(computer_move)
        return computer_move

    def computer_win(self):
        computer_moves = self.__occupied_coordinates[1::2]
        permuted_computer_moves = []
        for permuted_move in itertools.permutations(computer_moves):
            permuted_computer_moves.append(list(permuted_move))
        flag = False
        for move in self.__winning_coordinates:
            for computer_move in permuted_computer_moves:
                if move[0] in computer_move and move[1] in computer_move and move[2] in computer_move:
                    flag = True
                    break
            if flag is True:
                break
        if flag is True:
            print(f'occupied coordinates->{self.__occupied_coordinates}')
        return flag

    def user_win(self, update_brain_file=True):
        # filtering user moves from occupied coordinates
        user_moves = self.__occupied_coordinates[0::2]
        permuted_user_moves = []
        for permuted_move in itertools.permutations(user_moves):
            permuted_user_moves.append(list(permuted_move))
        flag = False
        for move in self.__winning_coordinates:
            for user_move in permuted_user_moves:
                if move[0] in user_move and move[1] in user_move and move[2] in user_move:
                    flag = True
                    break
            if flag is True:
                break
        # as user wins logging the move to brain for computer
        if flag is True and update_brain_file is True:
            self.__update_brain_file()
            print(f'occupied coordinates->{self.__occupied_coordinates}')

        return flag

    def is_draw(self):
        if self.computer_win() is False and self.user_win(False) is False:
            return True
        else:
            return False
