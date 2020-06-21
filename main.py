import chess
from time import sleep
from random import randint
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor


def minimax(maxDepth, board:chess.Board):
    with ProcessPoolExecutor(max_workers=8) as executor:

        moves = list(board.legal_moves)
        bestMove = None
        bestMoveValue = -1e9
        results = []
        for move in moves:
            results.append((move, executor.submit(_recursiveMiniMax, maxDepth-1, board.copy(), False, -1e9, 1e9)))

        for move, result in results:
            if result.result()>bestMoveValue:
                bestMoveValue = result.result()
                bestMove = move
        return bestMove

def _recursiveMiniMax(depth, board:chess.Board, isMaximazing, alpha, beta):
    if depth == 0 or board.is_game_over():
        return boardValue(board)
    else:
        moves = board.legal_moves
        bestMoveValue = (-1 if isMaximazing else 1) * 1e9
        op = max if isMaximazing else min
        for move in moves:
            board.push(move)
            bestMoveValue = op(bestMoveValue, _recursiveMiniMax(depth-1, board, not isMaximazing, alpha, beta))
            board.pop()
            if isMaximazing:
                alpha = max(alpha, bestMoveValue)
                if beta <= alpha:
                    return bestMoveValue
            else:
                beta = min(beta, bestMoveValue)
                if(beta <= alpha):
                    return bestMoveValue
        return bestMoveValue

def boardValue(board:chess.Board):
    value = 0
    for n in range(64):
        piece = str(board.piece_at(n))
        if piece.isupper():
            value += getPieceValue(piece)
        else:
            value -= getPieceValue(piece)
    return value

def getPieceValue(piece):
    if piece == None:
        return 0
    elif piece == "P" or piece == "p":
        return 10
    elif piece == "N" or piece == "n":
        return 30
    elif piece == "B" or piece == "b":
        return 30
    elif piece == "R" or piece == "r":
        return 50
    elif piece == "Q" or piece == "q":
        return 90
    elif piece == 'K' or piece == 'k':
        return 900
    else:
        return 0

board = chess.Board()
while not board.is_game_over():
    print(board)
    print()
    board.push(minimax(5, board))

    #sleep(0.5)