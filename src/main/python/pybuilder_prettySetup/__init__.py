"""
Most methods are modifications of original methods in
pybuilder.plugins.python.distutils

Their signatures are kept the same, so it'll be easier
to offer up a pull request to pybuilder in the future
"""
from pybuilder.core import use_plugin, init, task, Author
import os

def build_string_from_array(arr, keyName):
  indent = 6

  returnString = ""

  if len(arr) == 1:
    returnString += "['%s']" % arr[0]
  elif len(arr) > 1:
    returnString = "[\n"
    returnString += " " * indent
    returnString += "'"

    joinString = "',\n"
    joinString += " " * indent
    joinString += "'"

    returnString += joinString.join(arr)
    returnString += "'\n"
    returnString += " " * (indent - 2)
    returnString += "]"

  return returnString


def build_string_from_dict(d, keyName):
  indent = 6

  mapStrings = []

  for k, v in d:
    mapStrings.append("'%s': '%s'" % (k,v))

  returnString = ""

  if len(mapStrings) > 0:
    
    joinString = ",\n"
    joinString += " " * indent
    
    returnString += "\n"
    returnString += " " * indent
    returnString += joinString.join(mapStrings)
    returnString += "\n"
    returnString += " " * (indent - 2)
    returnString += "}"

  return returnString


def build_install_dependencies_string(project):
    dependencies = [
        dependency for dependency in project.dependencies
        if isinstance(dependency, Dependency) and not dependency.url]
    requirements = [
        requirement for requirement in project.dependencies
        if isinstance(requirement, RequirementsFile)]
    if not dependencies and not requirements:
        return ""

    dependencies = [format_single_dependency(dependency) for dependency in dependencies]
    requirements = [strip_comments(flatten_and_quote(requirement)) for requirement in requirements]
    flattened_requirements = [dependency for dependency_list in requirements for dependency in dependency_list]
    flattened_requirements_without_editables = [
        requirement for requirement in flattened_requirements if not is_editable_requirement(requirement)]

    dependencies.extend(flattened_requirements_without_editables)

    return build_string_from_array(dependencies, 'install_requires')


def build_dependency_links_string(project):
    dependency_links = [
        dependency for dependency in project.dependencies
        if isinstance(dependency, Dependency) and dependency.url]
    requirements = [
        requirement for requirement in project.dependencies
        if isinstance(requirement, RequirementsFile)]

    editable_links_from_requirements = []
    for requirement in requirements:
        editables = [editable for editable in flatten_and_quote(requirement) if is_editable_requirement(editable)]
        editable_links_from_requirements.extend(
            [editable.replace("--editable ", "").replace("-e ", "") for editable in editables])

    if not dependency_links and not requirements:
        return ""

    def format_single_dependency(dependency):
        return '"%s"' % dependency.url

    all_dependency_links = [link for link in map(format_single_dependency, dependency_links)]
    all_dependency_links.extend(editable_links_from_requirements)

    return build_string_from_array(all_dependency_links, 'dependency_links')


def build_scripts_string(project):
  scripts = [script for script in project.list_scripts()]
  
  scripts_dir = project.get_property("dir_dist_scripts")
  if scripts_dir:
    scripts = list(map(lambda s: os.path.join(scripts_dir, s), scripts))

  return build_string_from_array(scripts, 'scripts')
 
def build_data_files_string(project):
    data_files = project.files_to_install

    if not len(data_files):
        return ""

    return build_string_from_array(data_files, 'data_files')


def build_package_data_string(project):
  package_data = project.package_data
  if package_data == {}:
    return ""

  return build_string_from_dict(package_data, 'package_data')


def build_packages_string(project):

  pkgs = [pkg for pkg in project.list_packages()]

  return build_string_from_array(pkgs, 'packages')

  
def build_modules_string(project):

  mods = [mod for mod in project.list_modules()]

  return build_string_from_array(mods, 'modules')


def build_console_scripts_string(project):
  console_scripts = project.get_property('distutils_console_scripts', [])
  return build_string_from_array(console_scripts, 'console_scripts') 

def build_classifiers_string(project):
  classifiers = project.get_property('distutils_classifiers', [])
  return build_string_from_array(classifiers, 'classifiers')

@task('prettySetup')
def prettySetup(project):

    maps = [
      ('name', "'%s'" % project.name),
      ('version', "'%s'" % project.version),
      ('summary', "'%s'" % project.summary),
      ('description', "'%s'" % project.description),
      ('url', "'%s'" % project.url),
      ('license', "'%s'" % project.license)
    ]

    if len(project.authors) > 0:
      author = ", ".join(map(lambda a: a.name, project.authors))
      author_emails = ", ".join(map(lambda a: a.email, project.authors))
      maps.append(('author', "'%s'" % author))
      maps.append(('author_email', "'%s'" % author_emails))
    
    scripts = build_scripts_string(project)

    if scripts:
      maps.append(('scripts', scripts))

    packages = build_packages_string(project)
    if packages:
      maps.append(('packages', packages))

    modules = build_modules_string(project)
    if modules:
      maps.append(('modules', modules))

    classifiers = build_classifiers_string(project)
    if classifiers:
      maps.append(('classifiers', classifiers))

    console_scripts = build_console_scripts_string(project)
    if console_scripts:
      maps.append(('console_scripts', console_scripts))

    data_files = build_data_files_string(project)
    if data_files:
      maps.append(('data_files', data_files))

    package_data = build_package_data_string(project)
    if package_data:
      maps.append(('package_diata', package_data))

    dependencies = build_install_dependencies_string(project)
    if dependencies:
      maps.append(('dependencies', dependencies))

    dep_links = build_dependency_links_string(project)
    if dep_links:
      maps.append(('dependency_links', dep_links))

    setupTpl = "#!/usr/bin/env python\n"
    setupTpl += ("import os\ndel os.link"
                if project.get_property("distutils_issue8876_workaround_enabled")
                else "")

    setupTpl += "\nfrom %s import setup" % "setuptools" if project.get_property("distutils_use_setuptools") else "distutils.core"
    setupTpl += "\n\n"
    setupTpl += "if __name__ = '__main__':\n"
    setupTpl += "  setup(\n"

    lastMap = maps[-1]

    for keyName, value in maps:
      setupTpl += "    %s = %s" % (keyName, value)
      if lastMap[0] != keyName:
        setupTpl += ",\n"

    setupTpl += "\n  )\n"

    setup_script = project.expand_path("$dir_dist", "setup.py")
    with open(setup_script, "w") as setup_file:
      setup_file.write(setupTpl)

      os.chmod(setup_script, 0o755)
      
