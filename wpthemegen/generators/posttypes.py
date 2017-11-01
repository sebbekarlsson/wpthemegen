from wpthemegen.generators.generator import Generator
from jinja2 import Template


php_code = """
function custom_post_types() {

    {% for posttype in post_types %}
        register_post_type('{{posttype.name}}',
            [
                'labels' => [
                    'name' => __('{{posttype.name_multiple.title()}}'),
                    'singular_name' => __('{{posttype.name.title()}}')
                ],
                'public' => {{'true' if posttype.public else 'false'}},
                'has_archive' => {{'true' if posttype.has_archive else 'false'}},
                'supports' => [{% for support in posttype.supports %}'{{ support }}',{% endfor %}],
                'rewrite' => ['slug' => '{{ posttype.name_multiple }}']
            ]
        );
    {% endfor %}
}
add_action('init', 'custom_post_types', 0);
"""
php_template = Template(php_code)


class PosttypeGenerator(Generator):

    def __init__(self, config):
        Generator.__init__(self, config)
        self.php_code = php_template.render(
            post_types=config
        )

    def get_php(self):
        return self.php_code
