from tictactoe import TicTacToe

obj = TicTacToe()
obj.__int__()
user_input = ''
for step in range(obj.number_of_steps):
    if step % 2 == 0:
        while True:
            print(f'Enter coordinate to put your move')
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
        print(f'After step number {step + 1} user move --> {user_input} computer move --> {computer_move}')
    if obj.user_win() is True:
        print('User wins Exiting')
        break
    if obj.computer_win() is True:
        print('Computer wins Exiting')
        break
if obj.is_draw() is True:
    print('Draw')
