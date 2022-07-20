{.checks: off, optimization: speed, passc: "-O3".}

import std/[math, tables, algorithm, sequtils]

import nimpy

const COLOR_TRUNC = 128
const COLOR_TRUNC_TO = 256 div COLOR_TRUNC

const COLORAMA_COLORS = {
    "BLACK": "\x1b[30m",
    "RED": "\x1b[31m",
    "GREEN": "\x1b[32m",
    "YELLOW": "\x1b[33m",
    "BLUE": "\x1b[34m",
    "MAGENTA": "\x1b[35m",
    "CYAN": "\x1b[36m",
    "WHITE": "\x1b[37m",
    "LIGHTBLACK_EX": "\x1b[90m",
    "LIGHTRED_EX": "\x1b[91m",
    "LIGHTGREEN_EX": "\x1b[92m",
    "LIGHTYELLOW_EX": "\x1b[93m",
    "LIGHTBLUE_EX": "\x1b[94m",
    "LIGHTMAGENTA_EX": "\x1b[95m",
    "LIGHTCYAN_EX": "\x1b[96m",
    "LIGHTWHITE_EX": "\x1b[97m",
}.toTable

type Color = tuple[r, g, b: uint8]

proc genColors(): seq[Color] =
    result = @[]
    for r in 0 .. COLOR_TRUNC_TO:
        for g in 0 .. COLOR_TRUNC_TO:
            for b in 0 .. COLOR_TRUNC_TO:
                result.add((r.uint8, g.uint8, b.uint8))

proc dist(a: Color, b: Color): int =
    abs((b.r - a.r).int ^ 2 + (b.g - a.g).int ^ 2 + (b.b - a.b).int ^ 2)

proc cmpColorsTo(c: Color): (proc(a, b: Color): int) =
    proc cmpColors(x, y: Color): int =
        cmp(dist(x, c), dist(y, c))

    return cmpColors

proc truncColor(c: Color): Color {.inline.} =
    return (c.r div COLOR_TRUNC, c.g div COLOR_TRUNC, c.b div COLOR_TRUNC)

const RGB_TO_COLORAMA_NAME: Table[Color, string] = block:
    let rgbToColoramaName = {
        (196, 29, 17): "RED",
        (0, 193, 32): "GREEN",
        (199, 195, 38): "YELLOW",
        (10, 47, 196): "BLUE",
        (200, 57, 197): "MAGENTA",
        (1, 197, 198): "CYAN",
        (199, 199, 199): "WHITE",
        (104, 104, 104): "LIGHTBLACK_EX",
        (255, 110, 103): "LIGHTRED_EX",
        (96, 249, 102): "LIGHTGREEN_EX",
        (255, 252, 96): "LIGHTYELLOW_EX",
        (100, 111, 253): "LIGHTBLUE_EX",
        (255, 119, 255): "LIGHTMAGENTA_EX",
        (96, 253, 255): "LIGHTCYAN_EX",
        (255, 254, 245): "LIGHTWHITE_EX"
    }.toTable

    var result = initTable[Color, string]()
    for k, v in rgbToColoramaName.pairs:
        result[truncColor((k[0].uint8, k[1].uint8, k[2].uint8))] = v
    
    result

const ALL_RGB_TO_COLORAMA_NAME: Table[Color, string] = block:
    var result = initTable[Color, string]()

    var rgbVals = RGB_TO_COLORAMA_NAME.keys.toSeq

    for a in genColors():
        rgbVals.sort(cmpColorsTo(a))
        result[a] = RGB_TO_COLORAMA_NAME[rgbVals[0]]

    result

proc luminosity(c: Color): float {.inline.} =
    return 0.2126 * c.r.float + 0.7152 * c.g.float + 0.0722 * c.b.float

proc colorAprox(c: Color): string {.inline.} =
    return COLORAMA_COLORS[ALL_RGB_TO_COLORAMA_NAME[truncColor(c)]]

# # pointer nonsense :face_vomiting:
# proc `+`[T](p: ptr T, val: int) : ptr T {.inline.} =
#   cast[ptr T](cast[uint](p) + cast[uint](val * sizeof(T)))

# # add [] op for ptr garbage
# proc `[]`(p: RawPyBuffer, y: uint32, x: uint32, c: uint32): uint32 {.inline.} =
#     cast[ptr UncheckedArray[uint32]](p.buf)[y * (p.shape + 1)[].uint32 + x]

# proc `[]=`(p: RawPyBuffer, y: uint32, x: uint32, c: uint32, v: uint32) {.inline.} =
#     cast[ptr UncheckedArray[uint32]](p.buf)[y * (p.shape + 1)[].uint32 + x] = v

proc asciifyImage(image: openArray[seq[Color]], gradient: openArray[string]): string {.exportpy.} =
    let gradientLen = gradient.len.float
    result = ""
    var lastColoramaCode = "-1"

    for row in image:
        for color in row:
            var coloramaCode = colorAprox(color)

            if coloramaCode != lastColoramaCode:
                lastColoramaCode = coloramaCode
                result &= coloramaCode

            result &= gradient[int((luminosity(color) / 255) * gradientLen)]

        result &= "\n"
