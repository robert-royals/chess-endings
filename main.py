from enum import auto, Enum
import random
import chess
import chess.gaviota


class Style(Enum):
    EQUAL = auto()
    AT_MOST = auto()
    AT_LEAST = auto()


def generate_board(
    pieces,
    moves_to_mate,
    style=Style.EQUAL,
    to_move=chess.WHITE
):
    pieces = parse_piece_string(pieces)
    total_boards = 0
    legal_boards = 0
    with chess.gaviota.open_tablebase(
        "/home/aradesh/gaviota/{}".format(len(pieces))
    ) as tb:
        while 1:
            board = chess.Board(None)
            total_boards += 1
            for piece in pieces:
                while 1:
                    square = random.randint(0, 63)
                    if board.piece_at(square):
                        continue
                    else:
                        board.set_piece_at(square, piece)
                        break
            if not board.is_valid():
                continue
            legal_boards += 1
            dtm = tb.probe_dtm(board)
            if style == Style.EQUAL:
                if dtm == moves_to_mate*2 - 1:
                    print("Probed {} of {} boards".format(
                        legal_boards, total_boards
                    ))
                    return board
                else:
                    continue


piece_lookup = {
    'K': chess.KING,
    'Q': chess.QUEEN,
    'B': chess.BISHOP,
    'N': chess.KNIGHT,
    'R': chess.ROOK,
    'P': chess.PAWN,
}


def parse_piece_string(piece_string):
    pieces_per_player = piece_string.upper().split('V')
    if len(pieces_per_player) != 2:
        raise RuntimeError("Invalid piece string:", piece_string)
    white_str, black_str = pieces_per_player
    if len(white_str) > 16 or len(black_str) > 16:
        raise RuntimeError("Invalid piece string:", piece_string)
    white_pieces = [
        chess.Piece(piece_lookup[piece], chess.WHITE) for piece in white_str
    ]
    black_pieces = [
        chess.Piece(piece_lookup[piece], chess.BLACK) for piece in black_str
    ]
    return white_pieces + black_pieces


def main():
    for i in range(10):
        board = generate_board("KQvK", 4)
        print(board.fen())


if __name__ == "__main__":
    main()
