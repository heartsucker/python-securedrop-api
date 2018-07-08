import setuptools
import securedrop_api

from os import path

base_dir = path.abspath(path.dirname(__file__))

with open(path.join(base_dir, 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
    name='securedrop-api',
    version=securedrop_api.__version__,
    author='heartsucker',
    author_email='heartsucker@autistici.org',
    description='SecureDrop API client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'securedrop_api': 'securedrop_api'},
    packages=['securedrop_api'],
    platforms='any',
    python_requires='>=3.4',
    install_requires=[
        'json-serde',
    ],
    classifiers=(
        'Development Status :: 2 Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
)
