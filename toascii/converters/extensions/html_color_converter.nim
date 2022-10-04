import nimpy
import nimpy/[raw_buffers]

import nimpy_numpy
import converter_utils

proc colorToCss(c: Color): string {.inline.} =
    return "rgb(" & $c.r & "," & $c.g & "," & $c.b & ")"

proc asciifyImage(imgPyo: PyObject, gradient: openArray[string], saturation: float): string {.exportpy.} =
    var saturation = saturation
    if saturation > 1: saturation = 1
    elif saturation < -1: saturation = -1

    result = ""
    let gradientLen = gradient.len.float
    var lastColor = ""

    var imgBuf: RawPyBuffer
    imgPyo.getBuffer(imgBuf, PyBUF_WRITABLE or PyBuf_ND)
    defer: imgBuf.release()
    
    for rowIdx in 0 .. imgBuf.dimShape(0) - 1:
        for colIdx in 0 .. imgBuf.dimShape(1) - 1:
            let color = saturate(imgBuf[rowIdx, colIdx], saturation)
            let gChar = gradient[int((luminosity(color) / 255) * gradientLen)]
            let cssColor = colorToCss(color)

            if cssColor != lastColor:
                if lastColor != "":
                    result &= "</span>"

                lastColor = cssColor
                result &= "<span style=\"color:" & cssColor & "\">"

            result &= gChar

        result &= "<br>"
