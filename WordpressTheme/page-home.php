
            
            <?php
            /**
             * Template Name: home
             */
            ?>
            <?php
                $post = get_post(get_the_ID());
            ?>

            
<!DOCTYPE html>
<html>
    <head>
	<meta charset='UTF-8'/>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <?php wp_head(); ?>
    </head>
    <body>
        
    
        
    <nav class='navbar'>
        <a href='/home'>home</a>
        <a href='/about'>about</a>
        <a href='/contact'>contact</a>
    </nav>

        <div id='content'>
            
    <h1>This is the homepage</h1>

        </div>
        <footer>
            
    <p>A footer!</p>

        </footer>
    </body>
</html>
            