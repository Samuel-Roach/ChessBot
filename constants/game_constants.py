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

GAME_ICONS = {
        # Pieces
        PieceColor.BLACK: {
            PieceType.PAWN: {
                "icon": "♟︎",
                "image": "img/BLACK_PAWN.png"
                },
            PieceType.KNIGHT: {
                "icon": "♞",
                "image": "img/BLACK_KNIGHT.png"
                },
            PieceType.BISHOP: {
                "icon": "♝",
                "image": "img/BLACK_BISHOP.png"
                },
            PieceType.ROOK: {
                "icon": "♜",
                "image": "img/BLACK_ROOK.png"
                },
            PieceType.QUEEN: {
                "icon": "♛",
                "image": "img/BLACK_QUEEN.png"
                },
            PieceType.KING: {
                "icon": "♚",
                "image": "img/BLACK_KING.png"
                }
        },
        PieceColor.WHITE: {
            PieceType.PAWN: {
                "icon": "♙",
                "image": "img/WHITE_PAWN.png"
                },
            PieceType.KNIGHT: {
                "icon": "♘",
                "image": "img/WHITE_KNIGHT.png"
                },
            PieceType.BISHOP: {
                "icon": "♗",
                "image": "img/WHITE_BISHOP.png"
                },
            PieceType.ROOK: {
                "icon": "♖",
                "image": "img/WHITE_ROOK.png"
                },
            PieceType.QUEEN: {
                "icon": "♕",
                "image": "img/WHITE_QUEEN.png"
                },
            PieceType.KING: {
                "icon": "♔",
                "image": "img/WHITE_KING.png"
                }
        },

        # Tiles
        # Black
        "BLACK_TILE": "▮",
        "WHITE_TILE": "▯",

        "BOARD": "img/BOARD.png",
        "PREVIOUS_MOVE": "img/PREVIOUS_MOVE.png",
        "CHECK_MOVE": "img/CHECK_MOVE.png"
    }