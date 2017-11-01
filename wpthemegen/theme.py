from wpthemegen.generators.generator import Generator
from wpthemegen.generators.metaboxes import MetaboxGenerator
from wpthemegen.generators.posttypes import PosttypeGenerator
from wpthemegen.generators.settingspages import SettingsPageGenerator
from jinja2 import Template


php_functions_code = """
/* ===================== STYLES AND SCRIPTS ===================== */
function enqueue_the_styles() {
    wp_enqueue_style('ourplays-style', get_template_directory_uri() . '/static/css/style.css');
    wp_enqueue_script('ourplays-script', get_template_directory_uri() . '/static/js/final.js', array(), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'enqueue_the_styles');
/* ============================================================== */

/* ===================== POST TYPES ============================= */
{{ post_types_php }}
/* ============================================================== */

/* ===================== METABOXES ============================== */
{{ metaboxes_php }}
/* ============================================================== */
"""
php_functions_code_template = Template(php_functions_code)


class Theme(Generator):

    def __init__(self, config):
        Generator.__init__(self, config)
        if 'metaboxes' in config:
            self.metaboxGenerator = MetaboxGenerator(config['metaboxes'])

        if 'post_types' in config:
            self.posttypeGenerator = PosttypeGenerator(config['post_types'])

        if 'settings' in config:
            self.settingsPageGenerator = SettingsPageGenerator(config['settings'])

        self.php_code = php_functions_code_template.render(
            post_types_php=self.posttypeGenerator.get_php(),
            metaboxes_php=self.metaboxGenerator.get_php()
        )

    def get_php(self):
        return self.php_code
