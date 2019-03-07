from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name = 'decaptcher',
    version = '0.0.1',
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    maintainer='Gregory Petukhov',
    maintainer_email='lorien@lorien.name',
    url='https://github.com/lorien/decaptcher',
    description = 'Universal interface to multiple anti-captcha services',
    #long_description = open(os.path.join(ROOT, 'README.rst')).read(),
    packages = find_packages(exclude=['test']),
    download_url='https://github.com/lorien/decaptcher/releases',
    license = "MIT",
    install_requires = ['six'],
    keywords='captcha anti-captcha antigate rucaptcha 2captcha',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
