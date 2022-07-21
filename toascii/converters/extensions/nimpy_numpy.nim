import nimpy/[raw_buffers]

proc `+`[T](p: ptr T, val: int) : ptr T {.inline.} =
  cast[ptr T](cast[uint](p) + cast[uint](val * sizeof(T)))

proc dimShape*(imgBuf: RawPyBuffer, dim: int): uint32 {.inline.} =
    return (imgBuf.shape + dim)[].uint32

# [] operator for a 3d numpy array
proc `[]`*(imgBuf: RawPyBuffer, y: uint32, x: uint32, z: uint32): uint8 {.inline.} =
    let
        arr = cast[ptr UncheckedArray[uint8]](imgBuf.buf)
        xMax = imgBuf.dimShape(2)
        zMax = imgBuf.dimShape(1)

    return arr[y * xMax * zMax + x * xMax + z]

# []= operator for a 3d numpy array
proc `[]=`*(imgBuf: RawPyBuffer, y: uint32, x: uint32, z: uint32, v: uint8) {.inline.} =
    let
        arr = cast[ptr UncheckedArray[uint8]](imgBuf.buf)
        xMax = imgBuf.dimShape(2)
        zMax = imgBuf.dimShape(1)

    arr[y * xMax * zMax + x * xMax + z] = v
