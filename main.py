from tictactoe import TicTacToe

obj = TicTacToe()
for step in range(obj.number_of_steps):
    user_input = ''
    if step % 2 == 0:
        while True:
            print(f'Enter coordinate to put your move for step:{step + 1}')
            user_input = input()
            if len(user_input) > 2 or obj.check_user_input(user_input) is False:
                print('Invalid input, try again')
                continue
            else:
                break
        obj.input(step, user_input)
    else:
        # computer move
        computer_move = obj.get_move()
