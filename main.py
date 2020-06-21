import chess
from time import sleep
from random import randint
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

pieceLookUpValue = {
    "P":10,
    "N":30,
    "B":30,
    "R":50,
    "Q":90,
    'K':900,
    None:0
}

def minimax(maxDepth, board:chess.Board, isWhite):
    '''
    This function takes a board and returns the best move using minimax.

    isWhite refers to whether it is the white or black player currently searching for a move.
    The white player wants to maximize the value of the board, while the black player wants to minimize it. 
    '''
    moves = list(board.legal_moves)
    bestMove = None
    bestMoveValue = (-1 if isWhite else 1) * 1e9
    alpha = (-1 if isWhite else 1) * 1e9
    beta = -alpha
    # The moves in the root are checked in parallel, every moves subtree is sent to a separate process.
    results = []
    for move in moves:
        board.push(move)
        results.append((move, executor.submit(_recursiveMiniMax, maxDepth-1, board.copy(), not isWhite, alpha, beta)))
        board.pop()

    for move, result in tqdm(results):
        if isWhite: #If is white then we look for the maximum value
            if result.result() > bestMoveValue:
                bestMoveValue = result.result()
                bestMove = move
        else:
            if result.result() < bestMoveValue:
                bestMoveValue = result.result()
                bestMove = move
    print(bestMoveValue, "in", maxDepth, "moves")
    return bestMove

def _recursiveMiniMax(depth, board:chess.Board, isMaximazing, alpha, beta):
    if board.is_stalemate() or board.is_fivefold_repetition() or board.is_seventyfive_moves():
        return 0
    if board.is_checkmate():
        return (-1 if isMaximazing else 1) * 1e9
    elif depth == 0:
        return boardValue(board)

    else:
        bestMoveValue = (-1 if isMaximazing else 1) * 1e9
        op = max if isMaximazing else min
        
        for move in board.legal_moves:
            board.push(move)
            bestMoveValue = op(bestMoveValue, _recursiveMiniMax(depth-1, board, not isMaximazing, alpha, beta))
            board.pop()
            if isMaximazing:
                alpha = max(alpha, bestMoveValue)
                if beta <= alpha:
                    break
            else:
                beta = min(beta, bestMoveValue)
                if beta <= alpha:
                    break
        return bestMoveValue
        
def boardValue(board:chess.Board):
    value = 0
    for n in range(64):
        piece = str(board.piece_at(n))
        if piece == 'None': continue

        pieceValue = pieceLookUpValue[piece.upper()]
        #Good spots
        #012 34 567
        x = n%8
        y = n//8
        if x==3 or x == 4 and y == 3 or y==4:
            pieceValue *= 2

        if piece.isupper():
            value += pieceValue
        else:
            value -= pieceValue
        

    return value

DEPTH = 5
executor = ProcessPoolExecutor(max_workers=12)
if __name__ == "__main__":
    board = chess.Board()
    while not board.is_game_over():
        if board.turn:
            print("White's turn to move:")
        else:
            print("Black's turn to move:")
        print(board)
        print(boardValue(board))
        move = minimax(DEPTH, board, board.turn)
        print(move)
        board.push(move)
        print()
    print(board.result())
    print()
    if board.is_stalemate() or board.is_fivefold_repetition() or board.is_seventyfive_moves():
        print("Stalemate:", board.is_stalemate(), ", Fivefold:", board.is_fivefold_repetition(), ", seventyfive:", board.is_seventyfive_moves())
    #sleep(0.5)