def init_parser(subparsers):
    parser = subparsers.add_parser('run',
                                   help='Turn on one or more servers')
    parser.add_argument('apps', nargs="+", help="one or more apps to run")
    parser.set_defaults(cmd=cmd)
    return parser


def cmd(args):
    print 'run:', args
