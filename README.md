# pseudographics

A simple Python module for convering black-and-white bitmaps (contained in a 2D Numpy array) into pseudographics.


## Usage

```python
import numpy as np
from pseudographics import to_pseudographics, BlockSet

bitmap = np.array([
    [0, 1, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [0, 1, 1, 0],
])

text_lines = to_pseudographics(bitmap, BlockSet.BLOCKS_1X2)

print('\n'.join(text_lines))
```

## API

- ```python
  def to_pseudographics(bitmap: np.ndarray, block_set: BlockSet) -> list[str])
  ```
  Converts a black-and-white bitmap into lines of pseudographic characters.
  
  `bitmap` is a 2D Numpy array containing the bitmap. Zero-value pixels are considered background, non-zero ones are considered foreground.

  `block_set` specifies which Unicode characters to use.

  Returns a list of text lines of the same length.

- ```python
  class BlockSet
  ```
  Enum specifying which pseudographic Unicode characters to use to represent bitmap pixels:

  <table>
    <tr valign="top">
      <td><code>DOUBLE_BLOCKS</code></td>
      <td>
        Uses spaces and full-block characters from the <i>Block Elements</i> Unicode range.<br/>
        Each pixel of the bitmap is represented by two consecutive characters.<br/>
        In most monospaced fonts, the pixels look almost square.
      </td>
      <td><img src="img/double_blocks.png" width="268" /></td>
    </tr>
    <tr valign="top">
      <td><code>FULL_BLOCKS</code></td>
      <td>
        Uses spaces and full-block characters from the <i>Block Elements</i> Unicode range.<br/>
        Each character represents one pixel of the bitmap.<br/>
        In most monospaced fonts, the pixels look stretched vertically.
      </td>
      <td><img src="img/full_blocks.png" width="268" /></td>
    </tr>
    <tr valign="top">
      <td><code>BLOCKS_1X2</code></td>
      <td>
        Uses spaces and half-block characters from the <i>Block Elements</i> Unicode range.<br/>
        Each character represents two vertically arranged pixels of the bitmap.<br/>
        In most monospaced fonts, the pixels look almost square.
      </td>
      <td><img src="img/blocks_1x2.png" width="268" /></td>
    </tr>
    <tr valign="top">
      <td><code>BLOCKS_2X2</code></td>
      <td>
        Uses spaces and quarter-block characters from the <i>Block Elements</i> Unicode range.<br/>
        Each character represents a 2×2 pixel chunk of the bitmap.<br/>
        In most monospaced fonts, the pixels look stretched vertically.
      </td>
      <td><img src="img/blocks_2x2.png" width="268" /></td>
    </tr>
    <tr valign="top">
      <td><code>BLOCKS_2X3</code></td>
      <td>
        Uses sextant characters from the <i>Symbols for Legacy Computing</i><br/>
        Unicode range along with <i>Block Elements</i> characters and spaces.<br/>
        Introduced in Unicode 13 (2020), require newer fonts.<br/>
        Each character represents a 2×3 pixel chunk of the bitmap.<br/>
        In most monospaced fonts, the pixels look a bit stretched vertically.
      </td>
      <td><img src="img/blocks_2x3.png" width="268" /></td>
    </tr>
    <tr valign="top">
      <td><code>BLOCKS_2X4</code></td>
      <td>
        Uses octant characters from the <i>Symbols for Legacy Computing Supplement</i><br/>
        Unicode range along with <i>Block Elements</i> characters and spaces.<br/>
        Introduced in Unicode 16 (2024), require the newest fonts.<br/>
        Each character represents a 2×4 pixel chunk of the bitmap.<br/>
        In most monospaced fonts, the pixels look almost square.
      </td>
      <td><img src="img/blocks_2x4.png" width="268" /></td>
    </tr>
    <tr valign="top">
      <td><code>BRAILLE_2X4</code></td>
      <td>
        Uses characters from the <i>Braille Patterns</i> Unicode range.<br/>
        Each character represents a 2×4 pixel chunk of the bitmap.<br/>
        The pixels are usually round in shape with gaps in between.<br/>
        In some fonts, blank pixels are shown as empty circles.
      </td>
      <td><img src="img/braille_2x4.png" width="268" /></td>
    </tr>
  </table>
