def init_parser(subparsers):
    parser = subparsers.add_parser('status',
                                   help='Status of one or more servers')
    parser.add_argument('apps', nargs="+", help="one or more apps to run")
    parser.set_defaults(cmd=cmd)
    return parser


def cmd(args):
    print 'status:', args
