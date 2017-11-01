from wpthemegen.theme import Theme
import json
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--input", help="Input JSON config")
parser.add_argument("--output", help="Output directory")

args = parser.parse_args()


def generate():
    input_file = 'config.json'
    output_dir = '.'

    if args.input:
        input_file = args.input

    if args.output:
        output_dir = args.output

    json_content = ''
    with open(input_file) as configfile:
        json_content = json.loads(configfile.read())
    configfile.close()

    theme = Theme(json_content)

    print(theme.get_php())
