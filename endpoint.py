import logging
import time
import json
import multiprocessing
from multiprocessing import Pool
from flask import Flask, request
app = Flask(__name__)

logging.basicConfig(level='INFO')
log = logging.getLogger(__name__)

# load board and get board size
with open('board.txt') as f:
    board = json.loads(f.read())
board_size = len(board)

def define_response(return_msg, return_code):
    """
    Defines the response of the rest service
    :param return_msg: the message to return
    :param return_code: return code
    :return: the response body
    """
    response = app.response_class(
            response=return_msg,
            status=return_code,
            mimetype='application/json'
    )
    return response


def search_word(args):
    """
    Search a word in a list of string
    :param args:the word(string) to search and the list of string to search from
    :return: the word if found, else None
    """
    word, string_list = args
    # search the word in the string and reversed string
    for string in string_list:
        if word.upper() in string or word.upper() in string[::-1]:
            return word

def get_all_strings():
    """
    Get horizontal/vertical/diagonal strings
    :return: a list of all strings on the board
    """
    # Get horizontal strings
    h_strings = [''.join(x) for x in board]

    # Get vertical strings
    v_board = [[board[i][j] for i in range(board_size)] for j in range(board_size)]
    v_strings = [''.join(x) for x in v_board]

    # Get diagonal strings
    diag_list = []

    for b in [board, board[::-1]]:
        for offset in range(-board_size + 1, board_size):
            diag = [row[i + offset] for i, row in enumerate(b) if 0 <= i + offset < len(row)]
            diag_list.append(diag)
    diag_strings = [''.join(x) for x in diag_list]
    return v_strings+h_strings+diag_strings


@app.route('/8451/health', methods=['GET'])
def health():
    """
    ReST endpoint health check
    :return: service name and healthy status code
    """
    display = {'Service Name': '8451 words search',
               'Service Status': 'Ok'}
    return define_response(json.dumps(display), '200')

@app.route('/8451', methods=['GET'])
def words_search():
    """
    GET request for word search service
    :return: response
    """
    start_time = time.time()

    words = request.args.get('words')
    if not words:
        return define_response('words are required', '400')

    words_list = words.split(',')

    search_string_list = get_all_strings()

    # Search in parallel
    pool = Pool(multiprocessing.cpu_count())

    try:
        found_words = pool.imap_unordered(search_word, [(x, search_string_list) for x in words_list])
    except Exception as e:
        log.exception(e)
        return define_response('Unexpected exception!', '400')
    finally:
        pool.close()
        pool.join()

    output = [word for word in found_words if word is not None]

    log.info("--- Search done in %s minutes ---" % (round((time.time() - start_time) / 60, 2)))

    # Give proper output
    if len(output) > 0:
        return_msg = f'I found these words: {output}'
        return define_response(return_msg, '200')
    else:
        return_msg = f'No words found.'
        return define_response(return_msg, '400')


if __name__ == '__main__':
    app.run(debug=True)
