import abc


class Generator(object):

    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def generate(self):
        return
