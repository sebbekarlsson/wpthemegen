from setuptools import setup


setup(
    name='wpthemegen',
    version='0.1',
    install_requires=[
        'requests',
        'bs4',
        'Jinja2'
    ],
    packages=[
        'wpthemegen'
    ],
    entry_points={
        "console_scripts": [
            "wpthemegen = wpthemegen.generator:generate"
        ]
    }
)
