import std/[tables, math]

import nimpy
import nimpy/[raw_buffers]

import nimpy_numpy
import converter_utils

const COLOR_TRUNC = 128

proc truncColor(c: Color): Color {.inline.} =
    return (c.r div COLOR_TRUNC, c.g div COLOR_TRUNC, c.b div COLOR_TRUNC)

var RGB_TO_ASCII_CODE = initTable[Color, string]()
proc setRgbValuesMap(vals: seq[tuple[k: Color, v: string]]) {.exportpy.} =
    for p in vals:
        RGB_TO_ASCII_CODE[p.k] = p.v

proc colorAprox(c: Color): string {.inline.} =
    return RGB_TO_ASCII_CODE[truncColor(c)]

proc asciifyImage(imgPyo: PyObject, gradient: openArray[string], saturation: float): string {.exportpy.} =
    var saturation = saturation
    if saturation > 1: saturation = 1
    elif saturation < -1: saturation = -1

    result = ""
    let gradientLen = gradient.len.float
    var lastColoramaCode = "-1"

    var imgBuf: RawPyBuffer
    imgPyo.getBuffer(imgBuf, PyBUF_WRITABLE or PyBuf_ND)
    defer: imgBuf.release()
    
    for rowIdx in 0 .. imgBuf.dimShape(0) - 1:
        for colIdx in 0 .. imgBuf.dimShape(1) - 1:
            let color = saturate(imgBuf[rowIdx, colIdx], saturation)
            
            let coloramaCode = colorAprox(color)

            if coloramaCode != lastColoramaCode:
                lastColoramaCode = coloramaCode
                result &= coloramaCode

            result &= gradient[int((luminosity(color) / 255) * gradientLen)]

        result &= "\n"
