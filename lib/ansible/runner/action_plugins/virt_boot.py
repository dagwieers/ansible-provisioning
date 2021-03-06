# (c) 2012, Dag Wieers <dag@wieers.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
from ansible import utils
from ansible.runner.return_data import ReturnData

class ActionModule(object):

    def __init__(self, runner):
        self.runner = runner

    def run(self, conn, tmp, module_name, module_args, inject):
        ''' handler for file transfer operations '''

        # load up options
        options = utils.parse_kv(module_args)
        image = options.get('image', None)

        if image:
            # FIXME: We are transfering to /tmp in order to allow user qemu to have access
            tmp_image = os.path.join('/tmp', os.path.basename(image))
            conn.put_file(image, tmp_image)

            # fix file permissions when the copy is done as a different user
            if self.runner.sudo and self.runner.sudo_user != 'root':
                self.runner._low_level_exec_command(conn, "chmod a+r %s" % tmp_image, tmp)

            module_args = "%s image=%s" % (module_args, tmp_image)
        return self.runner._execute_module(conn, tmp, 'virt_boot', module_args, inject=inject)
