
class ABC:
    def asciify_pixel(self, p):  # takes [b, g, r]
        # assumes that there is a self.gradient, and a self.gradient_len
        # old gradient calculation
        #return self.gradient[int((((int(p[0]) + int(p[1]) + int(p[2])) / 3)*(self.gradient_len))/255)]
        return self.gradient[int((.2126*p[2] + .7152*p[1] + .0722*p[0])/255)]

    def asciify_row(self, row):  # returns the flattened map as a tuple
        # return (*map(self.asciify_pixel, row),)  # use * (all/star operator) to "flatten" the map() instead of a lazy map
        return map(self.asciify_pixel, row)

    def asciify_img(self, img):  # returns the actual finished, asciified image
        # uses a lazy map and flattens as it goes in the list comprehension
        return ''.join([f'\n{"".join(row)}' for row in map(self.asciify_row, img)])
