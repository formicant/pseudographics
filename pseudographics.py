from enum import Enum, auto
import numpy as np


class BlockSet(Enum):
    """ Enum specifying which pseudographic Unicode characters to use
        to represent bitmap pixels.
    """
    
    DOUBLE_BLOCKS = auto()
    """ Uses spaces and full-block characters from the ‘Block Elements’ Unicode range.
        Each pixel of the bitmap is represented by two consecutive characters.
        In most monospaced fonts, the pixels look almost square.
    """
    FULL_BLOCKS = auto()
    """ Uses spaces and full-block characters from the ‘Block Elements’ Unicode range.
        Each character represents one pixel of the bitmap.
        In most monospaced fonts, the pixels look stretched vertically.
    """
    BLOCKS_1X2 = auto()
    """ Uses spaces and half-block characters from the ‘Block Elements’ Unicode range.
        Each character represents two vertically arranged pixels of the bitmap.
        In most monospaced fonts, the pixels look almost square.
    """
    BLOCKS_2X2 = auto()
    """ Uses spaces and quarter-block characters from the ‘Block Elements’ Unicode range.
        Each character represents a 2×2 pixel chunk of the bitmap.
        In most monospaced fonts, the pixels look stretched vertically.
    """
    BLOCKS_2X3 = auto()
    """ Uses sextant characters from the ‘Symbols for Legacy Computing’
        Unicode range along with ‘Block Elements’ characters and spaces.
        Introduced in Unicode 13 (2020), require newer fonts.
        Each character represents a 2×3 pixel chunk of the bitmap.
        In most monospaced fonts, the pixels look a bit stretched vertically.
    """
    BLOCKS_2X4 = auto()
    """ Uses octant characters from the ‘Symbols for Legacy Computing Supplement’
        Unicode range along with ‘Block Elements’ characters and spaces.
        Introduced in Unicode 16 (2024), require the newest fonts.
        Each character represents a 2×4 pixel chunk of the bitmap.
        In most monospaced fonts, the pixels look almost square.
    """
    BRAILLE_2X4 = auto()
    """ Uses characters from the ‘Braille Patterns’ Unicode range.
        Each character represents a 2×4 pixel chunk of the bitmap.
        The pixels are usually round in shape with gaps in between.
        In some fonts, blank pixels are shown as empty circles.
    """


def to_pseudographics(bitmap: np.ndarray, block_set: BlockSet) -> list[str]:
    """ Converts a black-and-white bitmap into lines of pseudographic characters.
    
        `bitmap` is a 2D Numpy array containing the bitmap.
        Zero-value pixels are considered background, non-zero — foreground.
        
        `block_set` specifies which Unicode characters to use.
        
        Returns a list of text lines of the same length.
    """
    pseudographics = _pseudographics_by_block_set[block_set]
    blocks = pseudographics.bitmap_to_blocks(bitmap)
    return [''.join(row) for row in blocks]


class _Pseudographics:
    def __init__(self, blocks: list[str], pixel_order: list[list[int]]):
        self.blocks = np.array(blocks)
        self.matrix = 2 ** np.array(pixel_order)
        h, w = self.matrix.shape
        assert len(self.blocks) == 2 ** (h * w)
    
    def bitmap_to_blocks(self, bitmap: np.ndarray) -> np.ndarray:
        assert bitmap.ndim == 2
        bh, bw = bitmap.shape
        ch, cw = self.matrix.shape
        
        # binarize and pad
        bitmap = bitmap != 0
        if bh % ch != 0 or bw % cw != 0:
            bitmap = np.pad(bitmap, ((0, -bh % ch), (0, -bw % cw)))
            bh, bw = bitmap.shape
        
        # split the bitmap into `ch`-row chunks and each row into `cw`-pixel chunks:
        chunks = bitmap.reshape(bh // ch, ch, bw // cw, cw)
        # multiply every chunk by `matrix` using scalar multiplication:
        block_indices = np.tensordot(chunks, self.matrix, axes=((1, 3), (0, 1)))
        # return 2D array of pseudographic blocks:
        return self.blocks[block_indices]


_pseudographics_by_block_set = {
    BlockSet.DOUBLE_BLOCKS: _Pseudographics(
        ['  ', '██'],
        [[0]]),
    BlockSet.FULL_BLOCKS: _Pseudographics(
        [' ', '█'],
        [[0]]),
    BlockSet.BLOCKS_1X2: _Pseudographics(
        [' ', '▀', '▄', '█'],
        [
            [0],
            [1]
        ]),
    BlockSet.BLOCKS_2X2: _Pseudographics(
        list(' ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█'),
        [
            [0, 1],
            [2, 3],
        ]),
    BlockSet.BLOCKS_2X3: _Pseudographics(
        list(' 🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓▌🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧▐🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻█'),
        [
            [0, 1],
            [2, 3],
            [4, 5],
        ]),
    BlockSet.BLOCKS_2X4: _Pseudographics(
        list(
            ' 𜺨𜺫🮂𜴀▘𜴁𜴂𜴃𜴄▝𜴅𜴆𜴇𜴈▀𜴉𜴊𜴋𜴌🯦𜴍𜴎𜴏𜴐𜴑𜴒𜴓𜴔𜴕𜴖𜴗𜴘𜴙𜴚𜴛𜴜𜴝𜴞𜴟🯧𜴠𜴡𜴢𜴣𜴤𜴥𜴦𜴧𜴨𜴩𜴪𜴫𜴬𜴭𜴮𜴯𜴰𜴱𜴲𜴳𜴴𜴵🮅' +
            '𜺣𜴶𜴷𜴸𜴹𜴺𜴻𜴼𜴽𜴾𜴿𜵀𜵁𜵂𜵃𜵄▖𜵅𜵆𜵇𜵈▌𜵉𜵊𜵋𜵌▞𜵍𜵎𜵏𜵐▛𜵑𜵒𜵓𜵔𜵕𜵖𜵗𜵘𜵙𜵚𜵛𜵜𜵝𜵞𜵟𜵠𜵡𜵢𜵣𜵤𜵥𜵦𜵧𜵨𜵩𜵪𜵫𜵬𜵭𜵮𜵯𜵰' +
            '𜺠𜵱𜵲𜵳𜵴𜵵𜵶𜵷𜵸𜵹𜵺𜵻𜵼𜵽𜵾𜵿𜶀𜶁𜶂𜶃𜶄𜶅𜶆𜶇𜶈𜶉𜶊𜶋𜶌𜶍𜶎𜶏▗𜶐𜶑𜶒𜶓▚𜶔𜶕𜶖𜶗▐𜶘𜶙𜶚𜶛▜𜶜𜶝𜶞𜶟𜶠𜶡𜶢𜶣𜶤𜶥𜶦𜶧𜶨𜶩𜶪𜶫' +
            '▂𜶬𜶭𜶮𜶯𜶰𜶱𜶲𜶳𜶴𜶵𜶶𜶷𜶸𜶹𜶺𜶻𜶼𜶽𜶾𜶿𜷀𜷁𜷂𜷃𜷄𜷅𜷆𜷇𜷈𜷉𜷊𜷋𜷌𜷍𜷎𜷏𜷐𜷑𜷒𜷓𜷔𜷕𜷖𜷗𜷘𜷙𜷚▄𜷛𜷜𜷝𜷞▙𜷟𜷠𜷡𜷢▟𜷣▆𜷤𜷥█'),
        [
            [0, 1],
            [2, 3],
            [4, 5],
            [6, 7],
        ]),
    BlockSet.BRAILLE_2X4: _Pseudographics(
        [chr(i) for i in range(0x2800, 0x2900)],
        [
            [0, 3],
            [1, 4],
            [2, 5],
            [6, 7],
        ]),
}
