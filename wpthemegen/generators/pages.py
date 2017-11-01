from wpthemegen.generators.generator import Generator
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os


class PageGenerator(Generator):

    def __init__(self, config):
        Generator.__init__(self, config)
        self.php_code = ''

        self.env = Environment(
            loader=FileSystemLoader('./templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        if 'template' in config:
            self.template = self.env.get_template(config['template'])
            self.php_code = self.template.render()

    def get_php(self):
        return self.php_code
