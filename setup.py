from setuptools import setup, find_packages

requires = []
with open('requirements.txt') as reqfile:
    requires = reqfile.read().splitlines()

setup(
    name='meadows',
    version='0.0.1',
    description='Meadows Scythe: the Meadows Export & Analysis toolkit',
    url='https://github.com/meadowsresearch/scythe',
    long_description='Library for meadows users to preprocess downloaded data',
    long_description_content_type='text/plain',
    classifiers=[
      "Programming Language :: Python",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
    author='Jasper van den Bosch',
    author_email='jasper@meadows-research.com',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="tests",
)
