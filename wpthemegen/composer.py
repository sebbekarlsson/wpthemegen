import json
import os
import subprocess


def compose(config, composer_dir='.'):
    with open(os.path.join(composer_dir, 'composer.json'), 'w+') as composerfile:
        composerfile.write(json.dumps(config))
    composerfile.close()

    return subprocess.Popen(
        'composer install',
        cwd=composer_dir,
        shell=True
    )
