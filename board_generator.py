import sys
import string
import random
import json

if __name__ == '__main__':
    array_length = int(sys.argv[1])
    board = [[random.choice(string.ascii_letters.upper() + ' ') for x in range(array_length)] for y in
             range(array_length)]
    with open('board.txt', 'w') as f:
        f.write(json.dumps(board))