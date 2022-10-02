# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2015, 2017 Toshio Kuratomi <tkuratomi@ansible.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ast import arguments
from http.server import executable

__metaclass__ = type

DOCUMENTATION = """
    name: local
    short_description: execute on controller
    description:
        - This connection plugin allows ansible to execute tasks on the Ansible 'controller' instead of on a remote host.
    author: ansible (@core)
    version_added: historical
    extends_documentation_fragment:
        - connection_pipelining
    notes:
        - The remote user is ignored, the user with which the ansible CLI was executed is used instead.
"""

import os
import pty
import shutil
import subprocess
import fcntl
import shlex
from pathlib import Path

import ansible.constants as C
from ansible.errors import AnsibleError, AnsibleFileNotFound
from ansible.module_utils.compat import selectors
from ansible.module_utils.six import text_type, binary_type
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.connection import ConnectionBase
from ansible.utils.display import Display
from ansible.utils.path import unfrackpath

display = Display()

if (cmd_path := shutil.which("cmd.exe")) is None:
    raise AnsibleError("cmd.exe is not in PATH")
if (powershell_path := shutil.which("powershell.exe")) is None:
    raise AnsibleError("powershell.exe is not in PATH")
if (wslpath_path := shutil.which("wslpath")) is None:
    raise AnsibleError("wslpath is not in PATH")

def call(cmd,cwd=None):
    try:
        # https://docs.python.org/3/library/subprocess.html#exceptions
        return subprocess.run(
            shlex.split(cmd),
            cwd=cwd,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
        )
    except OSError as e:
        raise AnsibleError("failed to run %s, %s" % (cmd, to_native(e)))
# https://github.com/microsoft/WSL/issues/5718
def command_prompt(cmd,cwd=str(Path(cmd_path).parent)):
    cmd = cmd_path + " /c %s" % cmd
    return call(cmd,cwd)

def wslpath(path):
    """Convert Windows path to WSL path"""
    cmd = wslpath_path + " -u '%s'" % path
    return call(cmd).stdout.strip().decode()

def win_getuser():
    return command_prompt("echo %USERNAME%").stdout.strip()

def win_gettempdir():
    win_temp = command_prompt("echo %TEMP%").stdout.strip().decode()
    return wslpath(win_temp)


class Connection(ConnectionBase):
    """Local based connections"""
    
    transport = "wsl_local"
    has_pipelining = True

    def __init__(self, *args, **kwargs):

        super(Connection, self).__init__(*args, **kwargs)
        self.default_user = win_getuser()
        self.cwd = win_gettempdir() 
        self.module_implementation_preferences = (".ps1", ".exe", "")
        # always_pipeline_modules usage:  https://github.com/ansible/ansible/blob/789d29e89564f6c3e09e807d889b73e029d3edd9/lib/ansible/plugins/action/__init__.py#L1118
        self.always_pipeline_modules = False
        self.has_native_async = False
        self.allow_executable = False


    def _connect(self):
        """connect to the local host; nothing to do here"""

        # Because we haven't made any remote connection we're running as
        # the local user, rather than as whatever is configured in remote_user.
        self._play_context.remote_user = self.default_user
        if not self._connected:
            display.vvv(
                "ESTABLISH LOCAL CONNECTION FOR USER: {0}".format(
                    self._play_context.remote_user
                ),
                host=self._play_context.remote_addr,
            )
            self._connected = True
        return self

    def exec_command(self, cmd, in_data=None, sudoable=True):
        """run a command on the local host"""

        super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
        display.debug("in local.exec_command()")
        display.vvv(
            "EXEC {0}".format(to_text(cmd)), host=self._play_context.remote_addr
        )
        display.debug("opening command with Popen()")

        if isinstance(cmd, (text_type, binary_type)):
            cmd = to_bytes(cmd)
        else:
            cmd = map(to_bytes, cmd)

        p = subprocess.Popen(
            cmd,
            shell=isinstance(cmd, (text_type, binary_type)),
            executable=powershell_path,
            # https://github.com/microsoft/WSL/issues/5718
            cwd=self.cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        display.debug("done running command with Popen()")
        display.debug("getting output with communicate()")
        stdout, stderr = p.communicate(in_data)
        display.debug("done communicating")
        display.debug("done with local.exec_command()")
        return (p.returncode, stdout, stderr)

    def _copy(self, in_path, out_path):
        if not os.path.exists(to_bytes(in_path, errors="surrogate_or_strict")):
            raise AnsibleFileNotFound(
                "file or module does not exist: {0}".format(to_native(in_path))
            )
        try:
            shutil.copyfile(
                to_bytes(in_path, errors="surrogate_or_strict"),
                to_bytes(out_path, errors="surrogate_or_strict"),
            )
        except shutil.Error:
            raise AnsibleError(
                "failed to copy: {0} and {1} are the same".format(
                    to_native(in_path), to_native(out_path)
                )
            )
        except IOError as e:
            raise AnsibleError(
                "failed to transfer file to {0}: {1}".format(
                    to_native(out_path), to_native(e)
                )
            )

    def put_file(self, in_path, out_path):
        """transfer a file from wsl local to windows local"""

        super(Connection, self).put_file(in_path, out_path)

        in_path = unfrackpath(in_path, basedir=self.cwd)
        # out_path = unfrackpath(out_path, basedir=self.cwd)
        out_path = wslpath(out_path)
        display.vvv(
            "PUT {0} TO {1}".format(in_path, out_path),
            host=self._play_context.remote_addr,
        )
        self._copy(in_path, out_path)

    def fetch_file(self, in_path, out_path):
        """fetch a file from windows local to wsl local -- for compatibility"""

        super(Connection, self).fetch_file(in_path, out_path)

        # in_path = unfrackpath(in_path, basedir=self.cwd)
        in_path = wslpath(in_path)
        out_path = unfrackpath(out_path, basedir=self.cwd)
        display.vvv(
            "FETCH {0} TO {1}".format(in_path, out_path),
            host=self._play_context.remote_addr,
        )
        self._copy(in_path, out_path)

    def close(self):
        """ terminate the connection; nothing to do here """
        self._connected = False
