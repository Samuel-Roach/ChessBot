from src.chess_piece import ChessPiece, PieceType, PieceColor

""" A list of piece transforms for the threat matrix
    A tuple represents (x direction, y direction, steps)
"""
PIECE_TRANSFORMS = {
    PieceType.KNIGHT: {
        PieceColor.NEUTRAL: [
            (1, 2, 1),
            (2, 1, 1),
            (2, -1, 1),
            (1, -2, 1),
            (-1, -2, 1),
            (-2, -1, 1),
            (-2, 1, 1),
            (-1, 2, 1)
        ]
    },
    PieceType.ROOK: {
        PieceColor.NEUTRAL: [
            (-1, 0, 7),
            (1, 0, 7),
            (0, -1, 7),
            (0, 1, 7)
        ]
    },
    PieceType.BISHOP: {
        PieceColor.NEUTRAL: [
            (-1, -1, 7),
            (-1, 1, 7),
            (1, -1, 7),
            (1, 1, 7)
        ]
    },
    PieceType.QUEEN: {
        PieceColor.NEUTRAL: [
            (-1, 0, 7),
            (1, 0, 7),
            (0, -1, 7),
            (0, 1, 7),
            (-1, -1, 7),
            (-1, 1, 7),
            (1, -1, 7),
            (1, 1, 7)
        ]
    },
    PieceType.KING: {
        PieceColor.NEUTRAL: [
            (-1, -1, 1),
            (-1, 0, 1),
            (-1, 1, 1),
            (0, 1, 1),
            (1, 1, 1),
            (1, 0, 1),
            (1, -1, 1),
            (0, -1, 1)
        ]
    },
    PieceType.PAWN: {
        PieceColor.BLACK: [
            (-1, -1, 1),
            (1, -1, 1)
        ],
        PieceColor.WHITE: [
            (-1, 1, 1),
            (1, 1, 1)
        ]
    },
}