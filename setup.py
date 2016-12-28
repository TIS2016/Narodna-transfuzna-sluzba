from setuptools import setup, find_packages
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements/production.txt', session='hack')

setup(name='nts',
    version='1.0',
    author='HMST Solution',
    author_email='samommitas@gmail.com',
    url='https://github.com/TIS2016/Narodna-transfuzna-sluzba.git',
    packages=find_packages(),
    include_package_data=True,
    description='Non commercial application for NTS',
    install_requires=[str(ir.req) for ir in install_reqs],
)
