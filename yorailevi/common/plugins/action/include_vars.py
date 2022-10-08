# Copyright: (c) 2016, Allen Sanabria <asanabria@linuxdynasty.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from os import path, walk
from collections.abc import MutableMapping, MutableSequence
from json import dumps
import copy
import re

import ansible.constants as C
from ansible.errors import AnsibleError
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.action import ActionBase
# from ansible.utils.vars import combine_vars
from ansible.utils.vars import _validate_mutable_mappings
def combine_vars(a, b, merge=None, list_behavior='replace'):
    """
    Return a copy of dictionaries of variables based on configured hash behavior
    """

    if merge or merge is None and C.DEFAULT_HASH_BEHAVIOUR == "merge":
        return merge_obj(a, b,list_behavior=list_behavior)
    else:
        # HASH_BEHAVIOUR == 'replace'
        _validate_mutable_mappings(a, b)
        result = a.copy()
        result.update(b)
        return result
    
def _validate_mutable_sequences(a, b):
    """
    Internal convenience function to ensure arguments are MutableSequences

    This checks that all arguments are MutableSequences or raises an error

    :raises AnsibleError: if one of the arguments is not a MutableSequence
    """

    # If this becomes generally needed, change the signature to operate on
    # a variable number of arguments instead.

    if not (isinstance(a, MutableSequence) and isinstance(b, MutableSequence)):
        myvars = []
        for x in [a, b]:
            try:
                myvars.append(dumps(x))
            except Exception:
                myvars.append(to_native(x))
        raise AnsibleError("failed to combine variables, expected lists but got a '{0}' and a '{1}': \n{2}\n{3}".format(
            a.__class__.__name__, b.__class__.__name__, myvars[0], myvars[1])
        )

def merge_list(x, y, list_behavior='replace'):
    if list_behavior not in ('replace', 'keep', 'append', 'prepend', 'append_rp', 'prepend_rp'):
        raise AnsibleError("merge_hash: 'list_behavior' argument can only be equal to 'replace', 'keep', 'append', 'prepend', 'append_rp' or 'prepend_rp'")
    _validate_mutable_sequences(x,y)
    if list_behavior == 'replace':
        # replace x value by y's one as it has higher priority
        return y.copy()
    elif list_behavior == 'append':
        return x + y
    elif list_behavior == 'prepend':
        return y + x
    elif list_behavior == 'append_rp':
        # append all elements from y (high prio) to x (low prio)
        # and remove x elements that are also in y
        # we don't remove elements from x nor y that were already in double
        # (we assume that there is a reason if there where such double elements)
        # _rp stands for "remove present"
        return [z for z in x if z not in y] + y
    elif list_behavior == 'prepend_rp':
        # same as 'append_rp' but y elements are prepend
        return y + [z for z in x if z not in y]
    # else 'keep'
    #   keep x value even if y it's of higher priority
    #   it's done by not changing x[key]
    return x
    
def merge_hash(x, y, recursive=True, list_behavior='replace'):
    """
    Return a new dictionary result of the merges of y into x,
    so that keys from y take precedence over keys from x.
    (x and y aren't modified)
    """
    # verify x & y are dicts
    _validate_mutable_mappings(x, y)

    # to speed things up: if x is empty or equal to y, return y
    # (this `if` can be remove without impact on the function
    #  except performance)
    if x == {} or x == y:
        return y.copy()

    # in the following we will copy elements from y to x, but
    # we don't want to modify x, so we create a copy of it
    x = x.copy()

    # to speed things up: use dict.update if possible
    # (this `if` can be remove without impact on the function
    #  except performance)
    if not recursive and list_behavior == 'replace':
        x.update(y)
        return x

    # insert each element of y in x, overriding the one in x
    # (as y has higher priority)
    # we copy elements from y to x instead of x to y because
    # there is a high probability x will be the "default" dict the user
    # want to "patch" with y
    # therefore x will have much more elements than y
    for key, y_value in y.items():
        # if `key` isn't in x
        # update x and move on to the next element of y
        if key not in x:
            x[key] = y_value
            continue
        # from this point we know `key` is in x

        x_value = x[key]

        # if both x's element and y's element are dicts
        # recursively "combine" them or override x's with y's element
        # depending on the `recursive` argument
        # and move on to the next element of y
        if isinstance(x_value, MutableMapping) and isinstance(y_value, MutableMapping):
            if recursive:
                x[key] = merge_hash(x_value, y_value, recursive, list_behavior)
            else:
                x[key] = y_value
            continue
        if isinstance(x_value, MutableSequence) and isinstance(y_value, MutableSequence):
            x[key] = merge_list(x_value, y_value, list_behavior)
            continue
        # else just override x's element with y's one
        x[key] = y_value
    return x

def merge_obj(x, y, recursive=True, list_behavior='replace'):
    # Types are different. cannot merge. By default replace.
    if type(x) != type(y):
        return copy.copy(y)
    # Types are the same.
    if isinstance(x, MutableSequence):
        return merge_list(x,y,list_behavior)
    elif isinstance(x, MutableMapping):
        return merge_hash(x,y,recursive,list_behavior)
    else:
        # Types are not a mapping and not a sequence. Cannot merge. By default replace.
        return copy.copy(y)

class ActionModule(ActionBase):

    TRANSFERS_FILES = False

    VALID_FILE_EXTENSIONS = ['yaml', 'yml', 'json']
    VALID_DIR_ARGUMENTS = ['dir', 'depth', 'files_matching', 'ignore_files', 'extensions', 'ignore_unknown_extensions']
    VALID_FILE_ARGUMENTS = ['file', '_raw_params']
    VALID_ALL = ['name', 'hash_behaviour', 'list_behavior']

    def _set_dir_defaults(self):
        if not self.depth:
            self.depth = 0

        if self.files_matching:
            self.matcher = re.compile(r'{0}'.format(self.files_matching))
        else:
            self.matcher = None

        if not self.ignore_files:
            self.ignore_files = list()

        if isinstance(self.ignore_files, string_types):
            self.ignore_files = self.ignore_files.split()

        elif isinstance(self.ignore_files, dict):
            return {
                'failed': True,
                'message': '{0} must be a list'.format(self.ignore_files)
            }

    def _set_args(self):
        """ Set instance variables based on the arguments that were passed """

        self.hash_behaviour = self._task.args.get('hash_behaviour', 'merge')
        self.list_behavior = self._task.args.get('list_behavior', 'append' if self.hash_behaviour else 'replace')
        self.return_results_as_name = self._task.args.get('name', None)
        self.source_dir = self._task.args.get('dir', None)
        self.source_file = self._task.args.get('file', None)
        if not self.source_dir and not self.source_file:
            self.source_file = self._task.args.get('_raw_params')
            if self.source_file:
                self.source_file = self.source_file.rstrip('\n')

        self.depth = self._task.args.get('depth', None)
        self.files_matching = self._task.args.get('files_matching', None)
        self.ignore_unknown_extensions = self._task.args.get('ignore_unknown_extensions', False)
        self.ignore_files = self._task.args.get('ignore_files', None)
        self.valid_extensions = self._task.args.get('extensions', self.VALID_FILE_EXTENSIONS)

        # convert/validate extensions list
        if isinstance(self.valid_extensions, string_types):
            self.valid_extensions = list(self.valid_extensions)
        if not isinstance(self.valid_extensions, list):
            raise AnsibleError('Invalid type for "extensions" option, it must be a list')

    def run(self, tmp=None, task_vars=None):
        """ Load yml files recursively from a directory.
        """
        del tmp  # tmp no longer has any effect

        if task_vars is None:
            task_vars = dict()

        self.show_content = True
        self.included_files = []

        # Validate arguments
        dirs = 0
        files = 0
        for arg in self._task.args:
            if arg in self.VALID_DIR_ARGUMENTS:
                dirs += 1
            elif arg in self.VALID_FILE_ARGUMENTS:
                files += 1
            elif arg in self.VALID_ALL:
                pass
            else:
                raise AnsibleError('{0} is not a valid option in include_vars'.format(to_native(arg)))

        if dirs and files:
            raise AnsibleError("You are mixing file only and dir only arguments, these are incompatible")

        # set internal vars from args
        self._set_args()

        results = dict()
        failed = False
        if self.source_dir:
            self._set_dir_defaults()
            self._set_root_dir()
            if not path.exists(self.source_dir):
                failed = True
                err_msg = ('{0} directory does not exist'.format(to_native(self.source_dir)))
            elif not path.isdir(self.source_dir):
                failed = True
                err_msg = ('{0} is not a directory'.format(to_native(self.source_dir)))
            else:
                for root_dir, filenames in self._traverse_dir_depth():
                    failed, err_msg, updated_results = (self._load_files_in_dir(root_dir, filenames))
                    if failed:
                        break
                    results.update(updated_results)
        else:
            try:
                self.source_file = self._find_needle('vars', self.source_file)
                failed, err_msg, updated_results = (
                    self._load_files(self.source_file)
                )
                if not failed:
                    results.update(updated_results)

            except AnsibleError as e:
                failed = True
                err_msg = to_native(e)

        if self.return_results_as_name:
            scope = dict()
            scope[self.return_results_as_name] = results
            results = scope

        result = super(ActionModule, self).run(task_vars=task_vars)

        if failed:
            result['failed'] = failed
            result['message'] = err_msg
        elif self.hash_behaviour is not None and self.hash_behaviour != C.DEFAULT_HASH_BEHAVIOUR:
            merge_hashes = self.hash_behaviour == 'merge'
            for key, value in results.items():
                old_value = task_vars.get(key, None)
                results[key] = combine_vars(old_value, value, merge=merge_hashes, list_behavior=self.list_behavior)

        result['ansible_included_var_files'] = self.included_files
        result['ansible_facts'] = results
        result['_ansible_no_log'] = not self.show_content

        return result

    def _set_root_dir(self):
        if self._task._role:
            if self.source_dir.split('/')[0] == 'vars':
                path_to_use = (
                    path.join(self._task._role._role_path, self.source_dir)
                )
                if path.exists(path_to_use):
                    self.source_dir = path_to_use
            else:
                path_to_use = (
                    path.join(
                        self._task._role._role_path, 'vars', self.source_dir
                    )
                )
                self.source_dir = path_to_use
        else:
            if hasattr(self._task._ds, '_data_source'):
                current_dir = (
                    "/".join(self._task._ds._data_source.split('/')[:-1])
                )
                self.source_dir = path.join(current_dir, self.source_dir)

    def _log_walk(self, error):
        self._display.vvv('Issue with walking through "%s": %s' % (to_native(error.filename), to_native(error)))

    def _traverse_dir_depth(self):
        """ Recursively iterate over a directory and sort the files in
            alphabetical order. Do not iterate pass the set depth.
            The default depth is unlimited.
        """
        current_depth = 0
        sorted_walk = list(walk(self.source_dir, onerror=self._log_walk))
        sorted_walk.sort(key=lambda x: x[0])
        for current_root, current_dir, current_files in sorted_walk:
            current_depth += 1
            if current_depth <= self.depth or self.depth == 0:
                current_files.sort()
                yield (current_root, current_files)
            else:
                break

    def _ignore_file(self, filename):
        """ Return True if a file matches the list of ignore_files.
        Args:
            filename (str): The filename that is being matched against.

        Returns:
            Boolean
        """
        for file_type in self.ignore_files:
            try:
                if re.search(r'{0}$'.format(file_type), filename):
                    return True
            except Exception:
                err_msg = 'Invalid regular expression: {0}'.format(file_type)
                raise AnsibleError(err_msg)
        return False

    def _is_valid_file_ext(self, source_file):
        """ Verify if source file has a valid extension
        Args:
            source_file (str): The full path of source file or source file.
        Returns:
            Bool
        """
        file_ext = path.splitext(source_file)
        return bool(len(file_ext) > 1 and file_ext[-1][1:] in self.valid_extensions)

    def _load_files(self, filename, validate_extensions=False):
        """ Loads a file and converts the output into a valid Python dict.
        Args:
            filename (str): The source file.

        Returns:
            Tuple (bool, str, dict)
        """
        results = dict()
        failed = False
        err_msg = ''
        if validate_extensions and not self._is_valid_file_ext(filename):
            failed = True
            err_msg = ('{0} does not have a valid extension: {1}'.format(to_native(filename), ', '.join(self.valid_extensions)))
        else:
            b_data, show_content = self._loader._get_file_contents(filename)
            data = to_text(b_data, errors='surrogate_or_strict')

            self.show_content = show_content
            data = self._loader.load(data, file_name=filename, show_content=show_content)
            if not data:
                data = dict()
            if not isinstance(data, dict):
                failed = True
                err_msg = ('{0} must be stored as a dictionary/hash'.format(to_native(filename)))
            else:
                self.included_files.append(filename)
                results.update(data)

        return failed, err_msg, results

    def _load_files_in_dir(self, root_dir, var_files):
        """ Load the found yml files and update/overwrite the dictionary.
        Args:
            root_dir (str): The base directory of the list of files that is being passed.
            var_files: (list): List of files to iterate over and load into a dictionary.

        Returns:
            Tuple (bool, str, dict)
        """
        results = dict()
        failed = False
        err_msg = ''
        for filename in var_files:
            stop_iter = False
            # Never include main.yml from a role, as that is the default included by the role
            if self._task._role:
                if path.join(self._task._role._role_path, filename) == path.join(root_dir, 'vars', 'main.yml'):
                    stop_iter = True
                    continue

            filepath = path.join(root_dir, filename)
            if self.files_matching:
                if not self.matcher.search(filename):
                    stop_iter = True

            if not stop_iter and not failed:
                if self.ignore_unknown_extensions:
                    if path.exists(filepath) and not self._ignore_file(filename) and self._is_valid_file_ext(filename):
                        failed, err_msg, loaded_data = self._load_files(filepath, validate_extensions=True)
                        if not failed:
                            results.update(loaded_data)
                else:
                    if path.exists(filepath) and not self._ignore_file(filename):
                        failed, err_msg, loaded_data = self._load_files(filepath, validate_extensions=True)
                        if not failed:
                            results.update(loaded_data)

        return failed, err_msg, results
