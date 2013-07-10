from setuptools import setup, find_packages

setup(
    name = 'totalimpactwebapp',
    version = '0.2.0',
    packages = find_packages(),
    install_requires = [
        "Flask==0.7.2",
        "Jinja2==2.6",
        "gunicorn"
    ],
    url = '',
    author = 'ImpactStory',
    author_email = 'team@impactstory.org',
    license = 'MIT',
    classifiers = [
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

