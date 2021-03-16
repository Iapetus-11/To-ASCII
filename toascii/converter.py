
class Converter:
    def asciify(self, image):
        for row in image:
            for b, g, r in row:
                lumination = 0.2126 * r + 0.7152 * g + 0.0722 * b
                yield self.gradient[int((lumination / 255) * (self._gradient_len - 1))]

            yield "\n"
