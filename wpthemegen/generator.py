from wpthemegen.theme import Theme
import json
import argparse
import shutil
import os

parser = argparse.ArgumentParser()

parser.add_argument("--init", help="Generate templates")
parser.add_argument("--input", help="Input JSON config")
parser.add_argument("--output", help="Output directory")

args = parser.parse_args()

site_layout_html = """
<!DOCTYPE html>
<html>
    <head>
	<meta charset='UTF-8'/>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <?php wp_head(); ?>
    </head>
    <body>
        {% block head %}
        {% endblock %}
        <div id='content'>
            {% block body %}
            {% endblock %}
        </div>
        <footer>
            <?php wp_footer(); ?>
            {% block footer %}
            {% endblock %}
        </footer>
    </body>
</html>
"""


def generate():
    input_file = 'config.json'
    output_dir = '.'

    if args.input:
        input_file = args.input

    if args.output:
        output_dir = args.output
    
    if args.init:
        templates_dir = os.path.join(output_dir, 'templates')

        if os.path.isdir(templates_dir):
            print('templates directory already exists!')
            return False
        
        print('Generating base templates...')
        os.mkdir(templates_dir)
        with open('{}/layout.html'.format(templates_dir), 'w+') as layoutfile:
            layoutfile.write(site_layout_html)
        layoutfile.close()
        print('Done generating templates.')
        return True

    json_content = ''
    with open(input_file) as configfile:
        json_content = json.loads(configfile.read())
    configfile.close()

    theme = Theme(
        json_content,
        templates_dir=input_file.replace('config.json', './templates')
    )
    
    theme.generate(input_dir=input_file.replace('config.json', ''), output_dir=output_dir)
