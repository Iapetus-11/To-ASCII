import nimpy/[raw_buffers]

import nimpy_numpy

type
    Color* = tuple[r, g, b: uint8]
    HslColor* = tuple[h, s, l: float]

proc `[]`*(imgBuf: RawPyBuffer, y: uint32, x: uint32): Color {.inline.} =
    return (imgBuf[y, x, 2], imgBuf[y, x, 1], imgBuf[y, x, 0])

proc `[]=`*(imgBuf: RawPyBuffer, y: uint32, x: uint32, v: Color) {.inline.} =
    imgBuf[y, x, 0] = v.b
    imgBuf[y, x, 1] = v.g
    imgBuf[y, x, 2] = v.r

proc luminosity*(c: Color): float {.inline.} =
    return 0.2126 * c.r.float + 0.7152 * c.g.float + 0.0722 * c.b.float

proc rgb2hsl*(c: Color): HslColor {.inline.} =
    let
        r = c.r.float / 255.0
        g = c.g.float / 255.0
        b = c.b.float / 255.0
        cMin = min(r, min(g, b))
        cMax = max(r, max(g, b))
        delta = cMax - cMin

    var h, s, l: float = 0.0

    if delta == 0.0: h = 0.0
    elif cMax == r: h = ((g - b) / delta) mod 6.0
    elif cMax == g: h = ((b - r) / delta) + 2.0
    else: h = ((r - g) / delta) + 4.0

    h = round(h * 60.0)

    if (h < 0.0): h += 360.0

    l = (cMax + cMin) / 2.0

    if delta == 0.0: s = 0.0
    else: s = delta / (1 - abs(2.0 * l - 1.0))

    s *= 100.0
    l *= 100.0

    return (h, s, l)

proc hsl2rgb*(c: HslColor): Color {.inline.} =
    let
        h = c.h
        s = c.s / 100.0
        l = c.l / 100.0

    var
        r, g, b: float = 0.0
        c = (1.0 - abs(2 * l - 1.0)) * s
        x = c * (1.0 - abs((h / 60.0) mod 2.0 - 1.0))
        m = l - c / 2.0

    if (0 <= h and h < 60):
        r = c
        g = x
        b = 0
    elif (60 <= h and h < 120):
        r = x
        g = c
        b = 0
    elif (120 <= h and h < 180):
        r = 0
        g = c
        b = x
    elif (180 <= h and h < 240):
        r = 0
        g = x
        b = c
    elif (240 <= h and h < 300):
        r = x
        g = 0
        b = c
    elif (300 <= h and h < 360):
        r = c
        g = 0
        b = x

    r = round((r + m) * 255)
    g = round((g + m) * 255)
    b = round((b + m) * 255)

    return (r.uint8, g.uint8, b.uint8)

proc saturate*(c: Color, saturation: float): Color {.inline.} =
    var hsl = rgb2hsl(c)

    if saturation >= 0:
        let gray_factor = hsl.s / 100.0
        let var_interval = 100.0 - hsl.s
        hsl.s = hsl.s + saturation * var_interval * gray_factor
    else:
        hsl.s = hsl.s + saturation * hsl.s

    return hsl2rgb(hsl)
