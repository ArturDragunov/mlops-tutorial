from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines() # while reading requirements.txt, you get \n -> we drop it below
        requirements=[req.replace("\n","") for req in requirements]

        # each time we run pip install -r requirements.txt (with -e . present), it automatically triggers setup.py
        # and we build our package
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
name='mlproject',
version='0.0.1',
author='Artur',
author_email='dragunovartur61@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)