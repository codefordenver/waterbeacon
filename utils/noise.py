import numpy

class noise(object):

    def __init__(self, mean = 0.0, std = .1, samples = 1000):
        self.noise = numpy.random.normal(mean, std, size=samples)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        self.index += 1 
        if self.index >= len(self.noise):
            self.index = 0

        return self.noise[self.index]


if __name__ == "__main__":
 
    for n in noise(mean = 1, std = .2):
        print n