from wpthemegen.generators.generator import Generator
from wpthemegen.generators.metaboxes import MetaboxGenerator
from wpthemegen.generators.posttypes import PosttypeGenerator
from wpthemegen.generators.settingspages import SettingsPageGenerator
from wpthemegen.generators.pages import PageGenerator
from jinja2 import Template
import os
import shutil


php_functions_code = """
<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);


/* ===================== STYLES AND SCRIPTS ===================== */
function enqueue_the_styles() {
    wp_enqueue_style('{{ title }}-style', get_template_directory_uri() . '/static/css/style.css');
    wp_enqueue_script('{{ title }}-script', get_template_directory_uri() . '/static/js/final.js', array(), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'enqueue_the_styles');
/* ============================================================== */

/* ===================== POST TYPES ============================= */
{{ post_types_php }}
/* ============================================================== */

/* ===================== METABOXES ============================== */
{{ metaboxes_php }}
/* ============================================================== */
?>
"""
php_functions_code_template = Template(php_functions_code)


class Theme(Generator):

    def __init__(self, config, templates_dir='./templates'):
        Generator.__init__(self, config)
        self.page_generators = []
        self.title = 'WordpressTheme'

        if 'title' in config:
            self.title = config['title']

        if 'metaboxes' in config:
            self.metaboxGenerator = MetaboxGenerator(config['metaboxes'])

        if 'post_types' in config:
            self.posttypeGenerator = PosttypeGenerator(config['post_types'])

        if 'settings' in config:
            self.settingsPageGenerator = SettingsPageGenerator(config['settings'])

        if 'pages' in config:
            for page_config in config['pages']:
                self.page_generators.append(PageGenerator(page_config, templates_dir=templates_dir))

        self.php_code = php_functions_code_template.render(
            post_types_php=self.posttypeGenerator.get_php(),
            metaboxes_php=self.metaboxGenerator.get_php(),
            title=self.title
        )

    def get_php(self):
        return self.php_code

    def generate(self, input_dir, output_dir):
        output_dir = os.path.join(output_dir, self.title)

        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)

        os.mkdir(output_dir)

        static_src_dir = os.path.join(input_dir, 'static')

        if os.path.isdir(static_src_dir):
            shutil.copytree(static_src_dir, os.path.join(output_dir, 'static'))

        # == generate index.php file == #
        with open(os.path.join(output_dir, 'index.php'), 'w+') as _file:
            _file.write('')
        _file.close()

        # == generate style.css file == #
        with open(os.path.join(output_dir, 'style.css'), 'w+') as _file:
            _file.write('')
        _file.close()

        # == generate functions.php file == #
        with open(os.path.join(output_dir, 'functions.php'), 'w+') as _file:
            _file.write(self.get_php())
        _file.close()

        # == generate page templates == #
        for page in self.page_generators:
            filename = 'page.php' if not page.title else 'page-{}.php'.format(page.title)
            filename = os.path.join(output_dir, filename)

            with open(filename, 'w+') as _file:
                _file.write(page.get_php())
            _file.close()
