
class ABC:
    def asciify_pixel(self, p):  # takes [r, g, b]
        return self.gradient[int((((int(p[0]) + int(p[1]) + int(p[2])) / 3)*(self.gradient_len-1))/255)]

    def asciify_row(self, row):  # returns a flattened map (so a list)
        return (*map(self.asciify_pixel, row),)  # use * (all/star operator) to "flatten" the map() instead of a lazy map

    def asciify_img(self, img):  # returns a the actual asciified image
        # uses a lazy map and flattens as it goes in the list comprehension
        return ''.join([f'\n{"".join(row)}' for row in map(self.asciify_row, img)])
