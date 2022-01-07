from chess_piece import ChessPiece, PieceType, PieceColor

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
                "image": "board_src/BLACK_PAWN.png"
                },
            PieceType.KNIGHT: {
                "icon": "♞",
                "image": "board_src/BLACK_KNIGHT.png"
                },
            PieceType.BISHOP: {
                "icon": "♝",
                "image": "board_src/BLACK_BISHOP.png"
                },
            PieceType.ROOK: {
                "icon": "♜",
                "image": "board_src/BLACK_ROOK.png"
                },
            PieceType.QUEEN: {
                "icon": "♛",
                "image": "board_src/BLACK_QUEEN.png"
                },
            PieceType.KING: {
                "icon": "♚",
                "image": "board_src/BLACK_KING.png"
                }
        },
        PieceColor.WHITE: {
            PieceType.PAWN: {
                "icon": "♙",
                "image": "board_src/WHITE_PAWN.png"
                },
            PieceType.KNIGHT: {
                "icon": "♘",
                "image": "board_src/WHITE_KNIGHT.png"
                },
            PieceType.BISHOP: {
                "icon": "♗",
                "image": "board_src/WHITE_BISHOP.png"
                },
            PieceType.ROOK: {
                "icon": "♖",
                "image": "board_src/WHITE_ROOK.png"
                },
            PieceType.QUEEN: {
                "icon": "♕",
                "image": "board_src/WHITE_QUEEN.png"
                },
            PieceType.KING: {
                "icon": "♔",
                "image": "board_src/WHITE_KING.png"
                }
        },

        # Tiles
        # Black
        "BLACK_TILE": "▮",
        "WHITE_TILE": "▯",

        "BOARD": "board_src/board.png"
    }