from wpthemegen.generators.generator import Generator
from jinja2 import Environment, FileSystemLoader, select_autoescape


class PageGenerator(Generator):

    def __init__(self, config, templates_dir):
        Generator.__init__(self, config)
        self.php_code = ''
        self.title = 'page'

        if 'title' in config:
            self.title = config['title']

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        if 'template' in config:
            self.template = self.env.get_template(config['template'])
            self.php_code = """

            <?php
            /**
             * Template Name: {title}
             */
            ?>
            <?php
                $post = get_post(get_the_ID());
            ?>

            {page_content}
            """.format(page_content=self.template.render(), title=self.title)

    def get_php(self):
        return self.php_code
