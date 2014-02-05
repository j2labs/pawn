def init_parser(subparsers):
    parser = subparsers.add_parser('generate',
                                   help='generate a resource')
    parser.add_argument('resource', nargs=1, help="name of resources to generate")
    parser.set_defaults(cmd=cmd)
    return parser


def cmd(args):
    print 'generate:', args


def find_skel_dir(root_path):
    """Walks up from root_path, looking for a directory that matches the
    expected bpm skeleton directory path.
    """
    root_path = os.path.dirname(os.path.abspath(__file__))
    return walk_up_until(root_path, 'share/bpm/skel')


def find_template_files(dir, context_keys):
    """This function is a generator that searches every file in a directory,
    looking for evidence that template tags are being used. Each file is
    essentially grepped for each of the context keys.

    If a match is found, the files name and it's contents are returned. The
    assumption is that the receiving function will handle the replacement and
    write the new data to `filename`.
    """
    for parent, dnames, fnames in os.walk(dir):
        for fname in fnames:
            filename = os.path.join(parent, fname)
            if os.path.isfile(filename):
                with open(filename) as f:
                    text = f.read()
                    matched_keys = filter(lambda keyword: keyword in text,
                                          context_keys)
                    if len(matched_keys) > 0:
                        yield (filename, text)


def render_directory(dir, context):
    """This function renders a context on a directory.
    """
    ### Get the list of known keys
    context_keys = context.keys()
    
    for filename, text in find_template_files(dir, context_keys):
        render_and_write(filename, context, text)
        

def render_and_write(filename, context, text):
    """Opens a file and renders it according to the contents of `context`.
    """
    for key,value in context.items():
        items = text.split(key)
        text = value.join(items)
    with open(filename, 'w') as f:
        f.write(text)


def _apply_project(project_path, new_name):
    """Rename project dir in skel after project
    """
    ### Rename directory
    before = project_path + '/project'
    after = project_path + '/' + new_name
    shutil.move(before, after)

    ### Replace occurrences
    project_context = {
        '{{BPM_PROJECT_NAME}}': new_name,
    }

    render_directory(project_path, project_context)

    
def project_create(args):
    """Implements the `create` command. It essentially copies the contents of
    `bpm/settings/skel/` into a directory to bootstrap a project's design.
    """
    try:
        import pip
        import virtualenv
    except:
        response = raw_input(dep_statement_bpm)
    
    ### Find path to skel dir
    bpm_path = os.path.dirname(os.path.abspath(__file__))
    skel_path = find_skel_dir(bpm_path)

    if not skel_path:
        raise Exception("No project skeleton directory found!")

    ### Check validity of project name
    cwd = os.getcwd()
    project_path = '/'.join([cwd, args.name])
    if os.path.exists(project_path):
        error_msg = "Project directory %s already exists.  Please remove " \
                    "before continuing." % project_path
        raise ValueError(error_msg)

    ### Copy skel over
    shutil.copytree(skel_path, project_path)

    ### Rename project dir in skel after project
    _apply_project(project_path, args.name)        
