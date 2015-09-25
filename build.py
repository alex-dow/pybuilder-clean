import sys

sys.path.insert(0, 'src/main/python')

from pybuilder.core import Author, init, use_plugin
from pybuilder_prettySetup import prettySetup

use_plugin('python.core')
use_plugin("python.install_dependencies")
use_plugin('python.distutils')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.flake8')
use_plugin('python.pydev')

name = 'pybuilder_prettySetup'
version = '0.0.1'

authors = [Author('Alex Dowgailenko','adow@psikon.com')]
url = 'https://github.com/alex-dow/pybuilder_prettySetup'
description = 'Generates a nicer looking setup.py file'
license = 'Apache License, Version 2.0'
summary = 'PyBuilder PrettySetup Plugin'

default_task = ['clean', 'install_dependencies', 'analyze', 'publish', 'prettySetup']
#default_task = ['clean', 'install_dependencies', 'analyze', 'publish']

@init
def set_properties(project):
  project.set_property('flake8_verbose_output', True)

  project.set_property('coverage_break_build', False)


  project.get_property('distutils_commands').append('bdist_wheel')
  project.set_property('distutils_classifiers', [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7'
  ])

  project.build_depends_on_requirements('dev-requirements.txt')

  
