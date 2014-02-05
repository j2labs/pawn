import argparse
from .. import version as pawn_version
from . import run, terminate, status, generate


pawn_version = 'Pawn v%s' % (pawn_version)
pawn_description = 'Pawn command line tool'


def run_it():
    """Entry point for the `pawn` command
    """
    parser = argparse.ArgumentParser(description=pawn_description,
                                     version=pawn_version)
    parser.add_argument('-s', '--settings',
                        default="settings/",
                        action='store',
                        help='Location of settings directory')

    subparsers = parser.add_subparsers(dest='subcommands')
    subcommands = { run, terminate, status, generate }
    for sub_command in subcommands:
        sub_command.init_parser(subparsers)

    args = parser.parse_args()
    args.cmd(args)


def _import_module(module_dir, module_name, full_path_to_module):
    """http://bit.ly/PPf9y0
    """
    sys.path.insert(0, module_dir)
    module_obj = __import__(module_name)
    module_obj.__file__ = full_path_to_module
    sys.path.remove(module_dir)
    return module_obj


def import_dir(full_path_to_module):
    """Takes a full path to a directory and imports it as a module.
    """
    if full_path_to_module[-1] == os.sep:
        full_path_to_module = full_path_to_module[0:-1]
    module_dir, module_name = os.path.split(full_path_to_module)
    return _import_module(module_dir, module_name, full_path_to_module)


def import_file(full_path_to_module):
    """Takes a full path to a python file and imports it as a module.
    """
    module_dir, module_file = os.path.split(full_path_to_module)
    module_name, module_ext = os.path.splitext(module_file)
    return _import_module(module_dir, module_name, full_path_to_module)


def walk_up_until(root_path, sub_path):
    """Starts at `root_path` and basically loops through `cd ..` until it finds
    a directory that contains `sub_path`, or it reaches root.

    It returns the directory that had `sub_path` in it on success and returns
    None if nothing is found.
    """
    cur_dir = root_path
    while cur_dir != os.sep:
        potential_path = os.path.join(cur_dir, sub_path)
        if os.path.exists(potential_path):
            return potential_path
        cur_dir = os.path.dirname(cur_dir)
    return None


def find_settings():
    """This function attempts to discover the full path to a Brubeck project's
    settings file.
    """
    root_path = os.getcwd()
    path = walk_up_until(root_path, 'settings/')
    if path:
        return path


def load_settings():
    """Simple function that finds the settings file and returns a loaded python
    module.
    """
    settings_path = find_settings()
    settings = import_dir(settings_path)
    return settings
