"""This module patches the built in ExecCommand used by build systems to allow input via a keyboard shortcut"""

import os, sys
import thread
import subprocess
import time
import sublime_plugin

execmodule = __import__('exec')

def Monkeypatcher(name, bases, namespace):
    """http://mail.python.org/pipermail/python-dev/2008-January/076194.html"""
    base = bases[0]
    if hasattr(base, '__patched__'):
        return
    for name, value in namespace.iteritems():
        if name != "__metaclass__":
            setattr(base, name, value)
    base.__bases__ += bases[1:]
    setattr(base, '__patched__', True)
    return base

class PatchedAsyncProcess(execmodule.AsyncProcess):
    __metaclass__ = Monkeypatcher
    def __init__(self, arg_list, env, listener,
            # "path" is an option in build systems
            path="",
            # "shell" is an options in build systems
            shell=False):

        self.listener = listener
        self.killed = False

        self.start_time = time.time()

        # Hide the console window on Windows
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Set temporary PATH to locate executable in arg_list
        if path:
            old_path = os.environ["PATH"]
            # The user decides in the build system whether he wants to append $PATH
            # or tuck it at the front: "$PATH;C:\\new\\path", "C:\\new\\path;$PATH"
            os.environ["PATH"] = os.path.expandvars(path).encode(sys.getfilesystemencoding())

        proc_env = os.environ.copy()
        proc_env.update(env)
        for k, v in proc_env.iteritems():
            proc_env[k] = os.path.expandvars(v).encode(sys.getfilesystemencoding())

        # Patched here
        self.proc = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env, shell=shell)

        if path:
            os.environ["PATH"] = old_path

        if self.proc.stdout:
            thread.start_new_thread(self.read_stdout, ())

        if self.proc.stderr:
            thread.start_new_thread(self.read_stderr, ())

    # And patched here
    def give_input(self, value):
        os.write(self.proc.stdin.fileno(), value)
        if self.listener:
            self.listener.on_data(self, value)

if hasattr(execmodule, 'old_run_method'):
    oldRun = execmodule.old_run_method
else:
    oldRun = execmodule.ExecCommand.run
    execmodule.old_run_method = oldRun

# easy way of associating windows with their output panels, without causing strange bugs
panelsByWindow = {}

class PatchedExecCommand(execmodule.ExecCommand):
    __metaclass__ = Monkeypatcher
    def on_input_complete(self, value = None):
        """Show the output (which gets hidden) after taking the input"""
        if value is not None:
            self.proc.give_input(value + '\n')
            
        self.window.run_command("show_panel", {"panel": "output.exec"})
        self.window.focus_view(self.output_view)

    def run(self, give_input = False, **kwargs):
        """intercept a `give_input` argument before delegating to the real exec"""

        if give_input and hasattr(self, 'output_view'):
            lastline = self.output_view.substr(self.output_view.line(len(self.output_view)))
            self.window.show_input_panel(lastline or "", "", self.on_input_complete, None, self.on_input_complete)
            return
            
        oldRun(self, **kwargs)

        panelsByWindow[self.window.id()] = self.output_view.id()

class ExecInputListener(sublime_plugin.EventListener):
    """Accept input when output panel is focused"""
    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'build_selected':
            return view.id() == panelsByWindow[view.window().id()]
        else:
            return None