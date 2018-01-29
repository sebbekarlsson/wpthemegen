import json
import os
import subprocess


def compose(config, composer_dir='.'):
    with open(os.path.join(composer_dir, 'composer.json'), 'w+') as _file:
        _file.write(json.dumps(config))
    _file.close()

    return subprocess.Popen(
        'composer install',
        cwd=composer_dir,
        shell=True
    )
