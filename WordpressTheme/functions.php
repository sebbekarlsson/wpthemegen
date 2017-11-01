
<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);


/* ===================== STYLES AND SCRIPTS ===================== */
function enqueue_the_styles() {
    wp_enqueue_style('WordpressTheme-style', get_template_directory_uri() . '/static/css/style.css');
    wp_enqueue_script('WordpressTheme-script', get_template_directory_uri() . '/static/js/final.js', array(), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'enqueue_the_styles');
/* ============================================================== */

/* ===================== POST TYPES ============================= */

function custom_post_types() {

    
        register_post_type('book',
            [
                'labels' => [
                    'name' => __('Books'),
                    'singular_name' => __('Book')
                ],
                'public' => true,
                'has_archive' => true,
                'supports' => [],
                'rewrite' => ['slug' => 'books']
            ]
        );
    
        register_post_type('shelf',
            [
                'labels' => [
                    'name' => __('Shelfs'),
                    'singular_name' => __('Shelf')
                ],
                'public' => true,
                'has_archive' => true,
                'supports' => [],
                'rewrite' => ['slug' => 'shelfs']
            ]
        );
    
}
add_action('init', 'custom_post_types', 0);
/* ============================================================== */

/* ===================== METABOXES ============================== */


    
    function add_meta_box_Author() {
        
        add_meta_box(
            'author',      // Unique ID
            esc_html__( 'Author', 'author' ),    // Title
            'add_meta_box_Author_render',   // Callback function
            'book',         // Admin page (or post type)
            'side',         // Context
            'default'         // Priority
        );
        
    }
    add_action('add_meta_boxes', 'add_meta_box_Author');

    function add_meta_box_Author_render($post) {
        // Add a nonce field so we can check for it later.

        
            wp_nonce_field( '_name_nonce', '_name_nonce' );
            
            $value = get_post_meta($post->ID, '_name', true);

            echo '<textarea style="width:100%" id="_name" name="_name">' . esc_attr( $value ) . '</textarea>';

        
    }

    function save_Author_meta_box_data( $post_id ) {

        

            if (isset($_POST['_name_nonce'])) {
                if (wp_verify_nonce( $_POST['_name_nonce'], '_name_nonce' )) {
                    if (current_user_can( 'edit_page', $post_id ) ) {
                        if (isset($_POST['_name'])) {
                            $my_data = sanitize_text_field( $_POST['_name'] );
                            update_post_meta($post_id, '_name', $my_data);
                        }
                    }
                }
            }

        
    }

add_action( 'save_post', 'save_Author_meta_box_data' );


/* ============================================================== */
?>