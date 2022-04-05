from src.chess_piece import ChessPiece, PieceType, PieceColor

DEFAULT_BOARD = [
        [
            ChessPiece(PieceColor.WHITE, PieceType.ROOK),
            ChessPiece(PieceColor.WHITE, PieceType.KNIGHT),
            ChessPiece(PieceColor.WHITE, PieceType.BISHOP),
            ChessPiece(PieceColor.WHITE, PieceType.QUEEN),
            ChessPiece(PieceColor.WHITE, PieceType.KING),
            ChessPiece(PieceColor.WHITE, PieceType.BISHOP),
            ChessPiece(PieceColor.WHITE, PieceType.KNIGHT),
            ChessPiece(PieceColor.WHITE, PieceType.ROOK),
        ],
        [
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
            ChessPiece(PieceColor.WHITE, PieceType.PAWN),
        ],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
            ChessPiece(PieceColor.BLACK, PieceType.PAWN),
        ],
        [
            ChessPiece(PieceColor.BLACK, PieceType.ROOK),
            ChessPiece(PieceColor.BLACK, PieceType.KNIGHT),
            ChessPiece(PieceColor.BLACK, PieceType.BISHOP),
            ChessPiece(PieceColor.BLACK, PieceType.QUEEN),
            ChessPiece(PieceColor.BLACK, PieceType.KING),
            ChessPiece(PieceColor.BLACK, PieceType.BISHOP),
            ChessPiece(PieceColor.BLACK, PieceType.KNIGHT),
            ChessPiece(PieceColor.BLACK, PieceType.ROOK),
        ],
    ]

IMAGE_FOLDER = "img"
PIECE_FOLDER = f"{IMAGE_FOLDER}/piece"
BOARD_FOLDER = f"{IMAGE_FOLDER}/board"

GAME_ICONS = {
        # Pieces
        PieceColor.BLACK: {
            PieceType.PAWN: {
                "icon": "♟︎",
                "image": f"{PIECE_FOLDER}/default/BLACK_PAWN.png"
                },
            PieceType.KNIGHT: {
                "icon": "♞",
                "image": f"{PIECE_FOLDER}/default/BLACK_KNIGHT.png"
                },
            PieceType.BISHOP: {
                "icon": "♝",
                "image": f"{PIECE_FOLDER}/default/BLACK_BISHOP.png"
                },
            PieceType.ROOK: {
                "icon": "♜",
                "image": f"{PIECE_FOLDER}/default/BLACK_ROOK.png"
                },
            PieceType.QUEEN: {
                "icon": "♛",
                "image": f"{PIECE_FOLDER}/default/BLACK_QUEEN.png"
                },
            PieceType.KING: {
                "icon": "♚",
                "image": f"{PIECE_FOLDER}/default/BLACK_KING.png"
                }
        },
        PieceColor.WHITE: {
            PieceType.PAWN: {
                "icon": "♙",
                "image": f"{PIECE_FOLDER}/default/WHITE_PAWN.png"
                },
            PieceType.KNIGHT: {
                "icon": "♘",
                "image": f"{PIECE_FOLDER}/default/WHITE_KNIGHT.png"
                },
            PieceType.BISHOP: {
                "icon": "♗",
                "image": f"{PIECE_FOLDER}/default/WHITE_BISHOP.png"
                },
            PieceType.ROOK: {
                "icon": "♖",
                "image": f"{PIECE_FOLDER}/default/WHITE_ROOK.png"
                },
            PieceType.QUEEN: {
                "icon": "♕",
                "image": f"{PIECE_FOLDER}/default/WHITE_QUEEN.png"
                },
            PieceType.KING: {
                "icon": "♔",
                "image": f"{PIECE_FOLDER}/default/WHITE_KING.png"
                }
        },

        # Tiles
        # Black
        "BLACK_TILE": "▮",
        "WHITE_TILE": "▯",

        "BOARD": f"{BOARD_FOLDER}/light/BOARD.png",
        "PREVIOUS_MOVE": f"{BOARD_FOLDER}/light/PREVIOUS_MOVE.png",
        "CHECK_MOVE": f"{BOARD_FOLDER}/light/CHECK_MOVE.png"
    }

THEMES = {
    "board": {
        "light",
        "dark"
    },
    "piece": [
        "default",
        "simplified",
    ]
}