def init_parser(subparsers):
    parser = subparsers.add_parser('terminate',
                                   help='Terminate one or more servers')
    parser.add_argument('apps', nargs="+", help="one or more apps to terminate")
    parser.set_defaults(cmd=cmd)
    return parser


def cmd(args):
    print 'terminate:', args
