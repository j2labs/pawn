import cmd
import sys


class whatever(cmd.Cmd):
    """Rely on Python's `cmd` module for the interface to command development.
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'pawn> '

    def do_help(self, line):
        """This help menu"""
        if not line:
            print """
            run <server>: Start some pawn(s)
            stop <pid>:   Stop any pawn by its pid
            status:       Get info about running pawns
            mkenv:        Creates and install a pawn environment
            quit:         Exit pawn, if in interactive mode
            help <cmd>:   Get help on any command below
            version:      Pawn version info
            """
        else:
            cmd.Cmd.do_help(self, line)

    def do_EOF(self, line):
        """Exit pawn environment"""
        print 'bye'
        return True

    def default(self, line):
        print 'Command not recognized:', line
        print self.do_lhelp(None)

    def emptyline(self):
        pass

    def do_run(self, line):
        """Turn on some servers"""
        print 'run server,...,server'
        return False

    def do_stop(self, line):
        """Stop some servers"""
        print 'stop pid,...,pid'
        return False
        
    def do_status(self, line):
        """Shows the status of any running pawns"""
        print 'status'
        return False

    def do_mkenv(self, line):
        """Makes a new pawn environment"""
        return False

    def do_quit(self, line):
        """Exit pawn environment"""
        print 'bye'
        return True

    def do_version(self, line):
        from pawn import version
        print 'pawn v%s' % version
        return False


def run_it():
    """If an argument is provided, run it. If not, drop into a console"""
    arg_string = ' '.join(sys.argv[1:])
    w = whatever()
    if arg_string:
        w.onecmd(arg_string)
    else:
        try:
            w.cmdloop()
        except KeyboardInterrupt:
            print 'bye'
            sys.exit(0)


if __name__ == '__main__':
    run_it()
