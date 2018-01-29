from wpthemegen.generators.generator import Generator
from jinja2 import Template


php_code = """
{% for box in metaboxes %}
    function add_meta_box_{{ box.title }}() {
        add_meta_box(
            '{{ box.title.lower() }}',      // Unique ID
            esc_html__( '{{ box.title }}', '{{ box.title.lower() }}' ),    // Title
            'add_meta_box_{{ box.title }}_render',   // Callback function
            '{{ box.where }}',         // Admin page (or post type)
            '{{ box.context if box.context else 'side' }}',         // Context
            '{{ box.priority if box.priority else 'default' }}'         // Priority
        );
    }
    add_action('add_meta_boxes', 'add_meta_box_{{ box.title }}');

    function add_meta_box_{{ box.title }}_render($post) {
        // Add a nonce field so we can check for it later.

        {% for field in box.fields %}
            wp_nonce_field( '_{{ field.key }}_nonce', '_{{ field.key }}_nonce' );
            
            $value = get_post_meta($post->ID, '_{{ field.key }}', true);
            
            ?>
            <label for='_{{ field.key }}'>
                <p>{{ field.display_name }}</p>
                {% if field.type == 'textarea' or not field.type %}
                    <textarea style="width:100%" id="_{{ field.key }}" name="_{{ field.key }}"><?php echo esc_attr($value); ?></textarea>
                {% elif field.type == 'text' %}
                    <input type="text" id="_{{ field.key }}" name="_{{ field.key }}" value="<?php echo esc_attr($value); ?>"/>
                {% elif field.type == 'checkbox' %}
                    <input type="checkbox" id="_{{ field.key }}" name="_{{ field.key }}" <?php if (!empty($value)) { ?> checked <?php } ?>/>
                {% endif %}
            </label>
            <?php

        {% endfor %}
    }

    function save_{{ box.title }}_meta_box_data( $post_id ) {

        {% for field in box.fields %}

            if (isset($_POST['_{{ field.key }}_nonce'])) {
                if (wp_verify_nonce( $_POST['_{{ field.key }}_nonce'], '_{{ field.key }}_nonce' )) {
                    if (current_user_can( 'edit_page', $post_id ) ) {
                        if (isset($_POST['_{{ field.key }}'])) {
                            $my_data = sanitize_text_field( $_POST['_{{ field.key }}'] );
                            update_post_meta($post_id, '_{{ field.key }}', $my_data);
                        } else {
                            update_post_meta($post_id, '_{{ field.key }}', null);
                        }
                    }
                }
            }

        {% endfor %}
    }

add_action( 'save_post', 'save_{{ box.title }}_meta_box_data' );

{% endfor %}
"""
php_template = Template(php_code)


class MetaboxGenerator(Generator):

    def __init__(self, config):
        Generator.__init__(self, config)
        self.php_code = php_template.render(metaboxes=config)

    def get_php(self):
        return self.php_code
