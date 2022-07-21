import nimpy
import nimpy/[raw_buffers]

import nimpy_numpy
import converter_utils


proc asciifyImage(imgPyO: PyObject, gradient: openArray[string]): string {.exportpy.} =
    let gradientLen = gradient.len.float
    result = ""

    var imgBuf: RawPyBuffer
    imgPyo.getBuffer(imgBuf, PyBUF_WRITABLE or PyBuf_ND)
    defer: imgBuf.release()
    
    for rowIdx in 0 .. imgBuf.dimShape(0) - 1:
        for colIdx in 0 .. imgBuf.dimShape(1) - 1:
            let color = imgBuf[rowIdx, colIdx]

            result &= gradient[int((luminosity(color) / 255) * gradientLen)]

        result &= "\n"
