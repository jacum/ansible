#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Stephen Fromm <sfromm@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'core'}

DOCUMENTATION = '''
---
module: user
author:
- Stephen Fromm (@sfromm)
version_added: "0.2"
short_description: Manage user accounts
notes:
  - There are specific requirements per platform on user management utilities. However
    they generally come pre-installed with the system and Ansible will require they
    are present at runtime. If they are not, a descriptive error message will be shown.
  - For Windows targets, use the M(win_user) module instead.
description:
    - Manage user accounts and user attributes.
    - For Windows targets, use the M(win_user) module instead.
options:
    name:
        description:
            - Name of the user to create, remove or modify.
        required: true
        aliases: [ user ]
    uid:
        description:
            - Optionally sets the I(UID) of the user.
    comment:
        description:
            - Optionally sets the description (aka I(GECOS)) of user account.
    hidden:
        required: false
        type: bool
        description:
            - Darwin/OS X only, optionally hide the user from the login window and system preferences.
            - The default will be 'True' if the I(system) option is used.
        version_added: "2.6"
    non_unique:
        description:
            - Optionally when used with the -u option, this option allows to change the user ID to a non-unique value.
        type: bool
        default: "no"
        version_added: "1.1"
    seuser:
        description:
            - Optionally sets the seuser type (user_u) on selinux enabled systems.
        version_added: "2.1"
    group:
        description:
            - Optionally sets the user's primary group (takes a group name).
    groups:
        description:
            - Puts the user in  list of groups. When set to the empty string ('groups='),
              the user is removed from all groups except the primary group.
            - Before version 2.3, the only input format allowed was a 'comma separated string',
              now it should be able to accept YAML lists also.
    append:
        description:
            - If C(yes), will only add groups, not set them to just the list in I(groups).
        type: bool
        default: "no"
    shell:
        description:
            - Optionally set the user's shell.
            - On Mac OS X, before version 2.5, the default shell for non-system users was /usr/bin/false.
              Since 2.5, the default shell for non-system users on Mac OS X is /bin/bash.
    home:
        description:
            - Optionally set the user's home directory.
    skeleton:
        description:
            - Optionally set a home skeleton directory. Requires create_home option!
        version_added: "2.0"
    password:
        description:
            - Optionally set the user's password to this crypted value.
            - On Darwin/OS X systems, this value has to be cleartext. Beware of security issues.
            - See U(https://docs.ansible.com/ansible/faq.html#how-do-i-generate-crypted-passwords-for-the-user-module)
              for details on various ways to generate these password values.
    state:
        description:
            - Whether the account should exist or not, taking action if the state is different from what is stated.
        choices: [ absent, present ]
        default: present
    create_home:
        description:
            - Unless set to C(no), a home directory will be made for the user
              when the account is created or if the home directory does not exist.
            - Changed from C(createhome) to C(create_home) in version 2.5.
        type: bool
        default: 'yes'
        aliases: ['createhome']
    move_home:
        description:
            - If set to C(yes) when used with C(home=), attempt to move the user's old home
              directory to the specified directory if it isn't there already and the old home exists.
        type: bool
        default: "no"
    system:
        description:
            - When creating an account C(state=present), setting this to C(yes) makes the user a system account.
              This setting cannot be changed on existing users.
        type: bool
        default: "no"
    force:
        description:
            - This only affects C(state=absent), it forces removal of the user and associated directories on supported platforms.
              The behavior is the same as C(userdel --force), check the man page for C(userdel) on your system for details and support.
        type: bool
        default: "no"
    remove:
        description:
            - This only affects C(state=absent), it attempts to remove directories associated with the user.
              The behavior is the same as C(userdel --remove), check the man page for details and support.
        type: bool
        default: "no"
    login_class:
        description:
            - Optionally sets the user's login class, a feature of most BSD OSs.
    generate_ssh_key:
        description:
            - Whether to generate a SSH key for the user in question.
              This will B(not) overwrite an existing SSH key.
        type: bool
        default: "no"
        version_added: "0.9"
    ssh_key_bits:
        description:
            - Optionally specify number of bits in SSH key to create.
        default: default set by ssh-keygen
        version_added: "0.9"
    ssh_key_type:
        description:
            - Optionally specify the type of SSH key to generate.
              Available SSH key types will depend on implementation
              present on target host.
        default: rsa
        version_added: "0.9"
    ssh_key_file:
        description:
            - Optionally specify the SSH key filename. If this is a relative
              filename then it will be relative to the user's home directory.
        default: .ssh/id_rsa
        version_added: "0.9"
    ssh_key_comment:
        description:
            - Optionally define the comment for the SSH key.
        default: ansible-generated on $HOSTNAME
        version_added: "0.9"
    ssh_key_passphrase:
        description:
            - Set a passphrase for the SSH key.  If no
              passphrase is provided, the SSH key will default to
              having no passphrase.
        version_added: "0.9"
    update_password:
        description:
            - C(always) will update passwords if they differ.  C(on_create) will only set the password for newly created users.
        choices: [ always, on_create ]
        default: always
        version_added: "1.3"
    expires:
        description:
            - An expiry time for the user in epoch, it will be ignored on platforms that do not support this.
              Currently supported on GNU/Linux, FreeBSD, and DragonFlyBSD.
            - Since version 2.6 you can remove the expiry time specify a negative value. Currently supported on GNU/Linux and FreeBSD.
        version_added: "1.9"
    password_lock:
        description:
            - Lock the password (usermod -L, pw lock, usermod -C).
              BUT implementation differs on different platforms, this option does not always mean the user cannot login via other methods.
              This option does not disable the user, only lock the password. Do not change the password in the same task.
              Currently supported on Linux, FreeBSD, DragonFlyBSD, NetBSD.
        type: bool
        version_added: "2.6"
    local:
        description:
            - Forces the use of "local" command alternatives on platforms that implement it.
              This is useful in environments that use centralized authentification when you want to manipulate the local users.
              I.E. it uses `luseradd` instead of `useradd`.
            - This requires that these commands exist on the targeted host, otherwise it will be a fatal error.
        type: bool
        default: 'no'
        version_added: "2.4"
'''

EXAMPLES = '''
- name: Add the user 'johnd' with a specific uid and a primary group of 'admin'
  user:
    name: johnd
    comment: John Doe
    uid: 1040
    group: admin

- name: Add the user 'james' with a bash shell, appending the group 'admins' and 'developers' to the user's groups
  user:
    name: james
    shell: /bin/bash
    groups: admins,developers
    append: yes

- name: Remove the user 'johnd'
  user:
    name: johnd
    state: absent
    remove: yes

- name: Create a 2048-bit SSH key for user jsmith in ~jsmith/.ssh/id_rsa
  user:
    name: jsmith
    generate_ssh_key: yes
    ssh_key_bits: 2048
    ssh_key_file: .ssh/id_rsa

- name: Added a consultant whose account you want to expire
  user:
    name: james18
    shell: /bin/zsh
    groups: developers
    expires: 1422403387

- name: starting at version 2.6, modify user, remove expiry time
  user:
    name: james18
    expires: -1

'''

import grp
import os
import platform
import pwd
import shutil
import socket
import time

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import load_platform_subclass, AnsibleModule

try:
    import spwd
    HAVE_SPWD = True
except ImportError:
    HAVE_SPWD = False


class User(object):
    """
    This is a generic User manipulation class that is subclassed
    based on platform.

    A subclass may wish to override the following action methods:-
      - create_user()
      - remove_user()
      - modify_user()
      - ssh_key_gen()
      - ssh_key_fingerprint()
      - user_exists()

    All subclasses MUST define platform and distribution (which may be None).
    """

    platform = 'Generic'
    distribution = None
    SHADOWFILE = '/etc/shadow'
    SHADOWFILE_EXPIRE_INDEX = 7
    DATE_FORMAT = '%Y-%m-%d'

    def __new__(cls, *args, **kwargs):
        return load_platform_subclass(User, args, kwargs)

    def __init__(self, module):
        self.module = module
        self.state = module.params['state']
        self.name = module.params['name']
        self.uid = module.params['uid']
        self.hidden = module.params['hidden']
        self.non_unique = module.params['non_unique']
        self.seuser = module.params['seuser']
        self.group = module.params['group']
        self.comment = module.params['comment']
        self.shell = module.params['shell']
        self.password = module.params['password']
        self.force = module.params['force']
        self.remove = module.params['remove']
        self.create_home = module.params['create_home']
        self.move_home = module.params['move_home']
        self.skeleton = module.params['skeleton']
        self.system = module.params['system']
        self.login_class = module.params['login_class']
        self.append = module.params['append']
        self.sshkeygen = module.params['generate_ssh_key']
        self.ssh_bits = module.params['ssh_key_bits']
        self.ssh_type = module.params['ssh_key_type']
        self.ssh_comment = module.params['ssh_key_comment']
        self.ssh_passphrase = module.params['ssh_key_passphrase']
        self.update_password = module.params['update_password']
        self.home = module.params['home']
        self.expires = None
        self.password_lock = module.params['password_lock']
        self.groups = None
        self.local = module.params['local']

        if module.params['groups'] is not None:
            self.groups = ','.join(module.params['groups'])

        if module.params['expires'] is not None:
            try:
                self.expires = time.gmtime(module.params['expires'])
            except Exception as e:
                module.fail_json(msg="Invalid value for 'expires' %s: %s" % (self.expires, to_native(e)))

        if module.params['ssh_key_file'] is not None:
            self.ssh_file = module.params['ssh_key_file']
        else:
            self.ssh_file = os.path.join('.ssh', 'id_%s' % self.ssh_type)

    def execute_command(self, cmd, use_unsafe_shell=False, data=None, obey_checkmode=True):
        if self.module.check_mode and obey_checkmode:
            self.module.debug('In check mode, would have run: "%s"' % cmd)
            return (0, '', '')
        else:
            # cast all args to strings ansible-modules-core/issues/4397
            cmd = [str(x) for x in cmd]
            return self.module.run_command(cmd, use_unsafe_shell=use_unsafe_shell, data=data)

    def remove_user_userdel(self):
        if self.local:
            command_name = 'luserdel'
        else:
            command_name = 'userdel'

        cmd = [self.module.get_bin_path(command_name, True)]
        if self.force:
            cmd.append('-f')
        if self.remove:
            cmd.append('-r')
        cmd.append(self.name)

        return self.execute_command(cmd)

    def create_user_useradd(self):

        if self.local:
            command_name = 'luseradd'
        else:
            command_name = 'useradd'

        cmd = [self.module.get_bin_path(command_name, True)]

        if self.uid is not None:
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.seuser is not None:
            cmd.append('-Z')
            cmd.append(self.seuser)
        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            cmd.append('-g')
            cmd.append(self.group)
        elif self.group_exists(self.name):
            # use the -N option (no user group) if a group already
            # exists with the same name as the user to prevent
            # errors from useradd trying to create a group when
            # USERGROUPS_ENAB is set in /etc/login.defs.
            if os.path.exists('/etc/redhat-release'):
                dist = platform.dist()
                major_release = int(dist[1].split('.')[0])
                if major_release <= 5:
                    cmd.append('-n')
                else:
                    cmd.append('-N')
            elif os.path.exists('/etc/SuSE-release'):
                # -N did not exist in useradd before SLE 11 and did not
                # automatically create a group
                dist = platform.dist()
                major_release = int(dist[1].split('.')[0])
                if major_release >= 12:
                    cmd.append('-N')
            else:
                cmd.append('-N')

        if self.groups is not None and len(self.groups):
            groups = self.get_groups_set()
            cmd.append('-G')
            cmd.append(','.join(groups))

        if self.comment is not None:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.expires is not None:
            cmd.append('-e')
            cmd.append(time.strftime(self.DATE_FORMAT, self.expires))

        if self.password is not None:
            cmd.append('-p')
            cmd.append(self.password)

        if self.create_home:
            if not self.local:
                cmd.append('-m')

            if self.skeleton is not None:
                cmd.append('-k')
                cmd.append(self.skeleton)
        else:
            cmd.append('-M')

        if self.system:
            cmd.append('-r')

        cmd.append(self.name)
        return self.execute_command(cmd)

    def _check_usermod_append(self):
        # check if this version of usermod can append groups

        if self.local:
            command_name = 'lusermod'
        else:
            command_name = 'usermod'

        usermod_path = self.module.get_bin_path(command_name, True)

        # for some reason, usermod --help cannot be used by non root
        # on RH/Fedora, due to lack of execute bit for others
        if not os.access(usermod_path, os.X_OK):
            return False

        cmd = [usermod_path, '--help']
        (rc, data1, data2) = self.execute_command(cmd, obey_checkmode=False)
        helpout = data1 + data2

        # check if --append exists
        lines = to_native(helpout).split('\n')
        for line in lines:
            if line.strip().startswith('-a, --append'):
                return True

        return False

    def modify_user_usermod(self):

        if self.local:
            command_name = 'lusermod'
        else:
            command_name = 'usermod'

        cmd = [self.module.get_bin_path(command_name, True)]
        info = self.user_info()
        has_append = self._check_usermod_append()

        if self.uid is not None and info[2] != int(self.uid):
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            ginfo = self.group_info(self.group)
            if info[3] != ginfo[2]:
                cmd.append('-g')
                cmd.append(self.group)

        if self.groups is not None:
            # get a list of all groups for the user, including the primary
            current_groups = self.user_group_membership(exclude_primary=False)
            groups_need_mod = False
            groups = []

            if self.groups == '':
                if current_groups and not self.append:
                    groups_need_mod = True
            else:
                groups = self.get_groups_set(remove_existing=False)
                group_diff = set(current_groups).symmetric_difference(groups)

                if group_diff:
                    if self.append:
                        for g in groups:
                            if g in group_diff:
                                if has_append:
                                    cmd.append('-a')
                                groups_need_mod = True
                                break
                    else:
                        groups_need_mod = True

            if groups_need_mod:
                if self.append and not has_append:
                    cmd.append('-A')
                    cmd.append(','.join(group_diff))
                else:
                    cmd.append('-G')
                    cmd.append(','.join(groups))

        if self.comment is not None and info[4] != self.comment:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None and info[5] != self.home:
            cmd.append('-d')
            cmd.append(self.home)
            if self.move_home:
                cmd.append('-m')

        if self.shell is not None and info[6] != self.shell:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.expires is not None:

            current_expires = int(self.user_password()[1])

            if self.expires < time.gmtime(0):
                if current_expires > 0:
                    cmd.append('-e')
                    cmd.append('')
            else:
                # Convert days since Epoch to seconds since Epoch as struct_time
                current_expire_date = time.gmtime(current_expires * 86400)

                # Current expires is negative or we compare year, month, and day only
                if current_expires <= 0 or current_expire_date[:3] != self.expires[:3]:
                    cmd.append('-e')
                    cmd.append(time.strftime(self.DATE_FORMAT, self.expires))

        if self.password_lock:
            cmd.append('-L')
        elif self.password_lock is not None:
            cmd.append('-U')

        if self.update_password == 'always' and self.password is not None and info[1] != self.password:
            cmd.append('-p')
            cmd.append(self.password)

        # skip if no changes to be made
        if len(cmd) == 1:
            return (None, '', '')

        cmd.append(self.name)
        return self.execute_command(cmd)

    def group_exists(self, group):
        try:
            # Try group as a gid first
            grp.getgrgid(int(group))
            return True
        except (ValueError, KeyError):
            try:
                grp.getgrnam(group)
                return True
            except KeyError:
                return False

    def group_info(self, group):
        if not self.group_exists(group):
            return False
        try:
            # Try group as a gid first
            return list(grp.getgrgid(int(group)))
        except (ValueError, KeyError):
            return list(grp.getgrnam(group))

    def get_groups_set(self, remove_existing=True):
        if self.groups is None:
            return None
        info = self.user_info()
        groups = set(x.strip() for x in self.groups.split(',') if x)
        for g in groups.copy():
            if not self.group_exists(g):
                self.module.fail_json(msg="Group %s does not exist" % (g))
            if info and remove_existing and self.group_info(g)[2] == info[3]:
                groups.remove(g)
        return groups

    def user_group_membership(self, exclude_primary=True):
        ''' Return a list of groups the user belongs to '''
        groups = []
        info = self.get_pwd_info()
        for group in grp.getgrall():
            if self.name in group.gr_mem:
                # Exclude the user's primary group by default
                if not exclude_primary:
                    groups.append(group[0])
                else:
                    if info[3] != group.gr_gid:
                        groups.append(group[0])

        return groups

    def user_exists(self):
        try:
            if pwd.getpwnam(self.name):
                return True
        except KeyError:
            return False

    def get_pwd_info(self):
        if not self.user_exists():
            return False
        return list(pwd.getpwnam(self.name))

    def user_info(self):
        if not self.user_exists():
            return False
        info = self.get_pwd_info()
        if len(info[1]) == 1 or len(info[1]) == 0:
            info[1] = self.user_password()[0]
        return info

    def user_password(self):
        passwd = ''
        expires = ''
        if HAVE_SPWD:
            try:
                passwd = spwd.getspnam(self.name)[1]
                expires = spwd.getspnam(self.name)[7]
                return passwd, expires
            except KeyError:
                return passwd, expires

        if not self.user_exists():
            return passwd, expires
        elif self.SHADOWFILE:
            # Read shadow file for user's encrypted password string
            if os.path.exists(self.SHADOWFILE) and os.access(self.SHADOWFILE, os.R_OK):
                for line in open(self.SHADOWFILE).readlines():
                    if line.startswith('%s:' % self.name):
                        passwd = line.split(':')[1]
                        expires = line.split(':')[self.SHADOWFILE_EXPIRE_INDEX] or -1
        return passwd, expires

    def get_ssh_key_path(self):
        info = self.user_info()
        if os.path.isabs(self.ssh_file):
            ssh_key_file = self.ssh_file
        else:
            if not os.path.exists(info[5]) and not self.module.check_mode:
                raise Exception('User %s home directory does not exist' % self.name)
            ssh_key_file = os.path.join(info[5], self.ssh_file)
        return ssh_key_file

    def ssh_key_gen(self):
        info = self.user_info()
        try:
            ssh_key_file = self.get_ssh_key_path()
        except Exception as e:
            return (1, '', to_native(e))
        ssh_dir = os.path.dirname(ssh_key_file)
        if not os.path.exists(ssh_dir):
            if self.module.check_mode:
                return (0, '', '')
            try:
                os.mkdir(ssh_dir, int('0700', 8))
                os.chown(ssh_dir, info[2], info[3])
            except OSError as e:
                return (1, '', 'Failed to create %s: %s' % (ssh_dir, to_native(e)))
        if os.path.exists(ssh_key_file):
            return (None, 'Key already exists', '')
        cmd = [self.module.get_bin_path('ssh-keygen', True)]
        cmd.append('-t')
        cmd.append(self.ssh_type)
        if self.ssh_bits > 0:
            cmd.append('-b')
            cmd.append(self.ssh_bits)
        cmd.append('-C')
        cmd.append(self.ssh_comment)
        cmd.append('-f')
        cmd.append(ssh_key_file)
        cmd.append('-N')
        if self.ssh_passphrase is not None:
            cmd.append(self.ssh_passphrase)
        else:
            cmd.append('')

        (rc, out, err) = self.execute_command(cmd)
        if rc == 0 and not self.module.check_mode:
            # If the keys were successfully created, we should be able
            # to tweak ownership.
            os.chown(ssh_key_file, info[2], info[3])
            os.chown('%s.pub' % ssh_key_file, info[2], info[3])
        return (rc, out, err)

    def ssh_key_fingerprint(self):
        ssh_key_file = self.get_ssh_key_path()
        if not os.path.exists(ssh_key_file):
            return (1, 'SSH Key file %s does not exist' % ssh_key_file, '')
        cmd = [self.module.get_bin_path('ssh-keygen', True)]
        cmd.append('-l')
        cmd.append('-f')
        cmd.append(ssh_key_file)

        return self.execute_command(cmd, obey_checkmode=False)

    def get_ssh_public_key(self):
        ssh_public_key_file = '%s.pub' % self.get_ssh_key_path()
        try:
            f = open(ssh_public_key_file)
            ssh_public_key = f.read().strip()
            f.close()
        except IOError:
            return None
        return ssh_public_key

    def create_user(self):
        # by default we use the create_user_useradd method
        return self.create_user_useradd()

    def remove_user(self):
        # by default we use the remove_user_userdel method
        return self.remove_user_userdel()

    def modify_user(self):
        # by default we use the modify_user_usermod method
        return self.modify_user_usermod()

    def create_homedir(self, path):
        if not os.path.exists(path):
            if self.skeleton is not None:
                skeleton = self.skeleton
            else:
                skeleton = '/etc/skel'

            if os.path.exists(skeleton):
                try:
                    shutil.copytree(skeleton, path, symlinks=True)
                except OSError as e:
                    self.module.exit_json(failed=True, msg="%s" % to_native(e))
        else:
            try:
                os.makedirs(path)
            except OSError as e:
                self.module.exit_json(failed=True, msg="%s" % to_native(e))

    def chown_homedir(self, uid, gid, path):
        try:
            os.chown(path, uid, gid)
            for root, dirs, files in os.walk(path):
                for d in dirs:
                    os.chown(os.path.join(root, d), uid, gid)
                for f in files:
                    os.chown(os.path.join(root, f), uid, gid)
        except OSError as e:
            self.module.exit_json(failed=True, msg="%s" % to_native(e))


# ===========================================

class FreeBsdUser(User):
    """
    This is a FreeBSD User manipulation class - it uses the pw command
    to manipulate the user database, followed by the chpass command
    to change the password.

    This overrides the following methods from the generic class:-
      - create_user()
      - remove_user()
      - modify_user()
    """

    platform = 'FreeBSD'
    distribution = None
    SHADOWFILE = '/etc/master.passwd'
    SHADOWFILE_EXPIRE_INDEX = 6
    DATE_FORMAT = '%d-%b-%Y'

    def remove_user(self):
        cmd = [
            self.module.get_bin_path('pw', True),
            'userdel',
            '-n',
            self.name
        ]
        if self.remove:
            cmd.append('-r')

        return self.execute_command(cmd)

    def create_user(self):
        cmd = [
            self.module.get_bin_path('pw', True),
            'useradd',
            '-n',
            self.name,
        ]

        if self.uid is not None:
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.comment is not None:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            cmd.append('-d')
            cmd.append(self.home)

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            cmd.append('-g')
            cmd.append(self.group)

        if self.groups is not None:
            groups = self.get_groups_set()
            cmd.append('-G')
            cmd.append(','.join(groups))

        if self.create_home:
            cmd.append('-m')

            if self.skeleton is not None:
                cmd.append('-k')
                cmd.append(self.skeleton)

        if self.shell is not None:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.login_class is not None:
            cmd.append('-L')
            cmd.append(self.login_class)

        if self.expires is not None:
            cmd.append('-e')
            cmd.append(time.strftime(self.DATE_FORMAT, self.expires))

        # system cannot be handled currently - should we error if its requested?
        # create the user
        (rc, out, err) = self.execute_command(cmd)
        if rc is not None and rc != 0:
            self.module.fail_json(name=self.name, msg=err, rc=rc)

        # we have to set the password in a second command
        if self.password is not None:
            cmd = [
                self.module.get_bin_path('chpass', True),
                '-p',
                self.password,
                self.name
            ]
            return self.execute_command(cmd)

        return (rc, out, err)

    def modify_user(self):
        cmd = [
            self.module.get_bin_path('pw', True),
            'usermod',
            '-n',
            self.name
        ]
        cmd_len = len(cmd)
        info = self.user_info()

        if self.uid is not None and info[2] != int(self.uid):
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.comment is not None and info[4] != self.comment:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            if (info[5] != self.home and self.move_home) or (not os.path.exists(self.home) and self.createhome):
                cmd.append('-m')
            cmd.append('-d')
            cmd.append(self.home)

            if self.skeleton is not None:
                cmd.append('-k')
                cmd.append(self.skeleton)

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            ginfo = self.group_info(self.group)
            if info[3] != ginfo[2]:
                cmd.append('-g')
                cmd.append(self.group)

        if self.shell is not None and info[6] != self.shell:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.login_class is not None:
            # find current login class
            user_login_class = None
            if os.path.exists(self.SHADOWFILE) and os.access(self.SHADOWFILE, os.R_OK):
                for line in open(self.SHADOWFILE).readlines():
                    if line.startswith('%s:' % self.name):
                        user_login_class = line.split(':')[4]

            # act only if login_class change
            if self.login_class != user_login_class:
                cmd.append('-L')
                cmd.append(self.login_class)

        if self.groups is not None:
            current_groups = self.user_group_membership()
            groups = self.get_groups_set()

            group_diff = set(current_groups).symmetric_difference(groups)
            groups_need_mod = False

            if group_diff:
                if self.append:
                    for g in groups:
                        if g in group_diff:
                            groups_need_mod = True
                            break
                else:
                    groups_need_mod = True

            if groups_need_mod:
                cmd.append('-G')
                new_groups = groups
                if self.append:
                    new_groups = groups | set(current_groups)
                cmd.append(','.join(new_groups))

        if self.expires is not None:

            current_expires = int(self.user_password()[1])

            if self.expires < time.gmtime(0):
                if current_expires > 0:
                    cmd.append('-e')
                    cmd.append('0')
            else:
                # Convert days since Epoch to seconds since Epoch as struct_time
                current_expire_date = time.gmtime(current_expires)

                # Current expires is negative or we compare year, month, and day only
                if current_expires <= 0 or current_expire_date[:3] != self.expires[:3]:
                    cmd.append('-e')
                    cmd.append(time.strftime(self.DATE_FORMAT, self.expires))

        # modify the user if cmd will do anything
        if cmd_len != len(cmd):
            (rc, out, err) = self.execute_command(cmd)
            if rc is not None and rc != 0:
                self.module.fail_json(name=self.name, msg=err, rc=rc)
        else:
            (rc, out, err) = (None, '', '')

        # we have to set the password in a second command
        if self.update_password == 'always' and self.password is not None and info[1] != self.password:
            cmd = [
                self.module.get_bin_path('chpass', True),
                '-p',
                self.password,
                self.name
            ]
            return self.execute_command(cmd)

        # we have to lock/unlock the password in a distinct command
        if self.password_lock:
            cmd = [
                self.module.get_bin_path('pw', True),
                'lock',
                '-n',
                self.name
            ]
            if self.uid is not None and info[2] != int(self.uid):
                cmd.append('-u')
                cmd.append(self.uid)
            return self.execute_command(cmd)
        elif self.password_lock is not None:
            cmd = [
                self.module.get_bin_path('pw', True),
                'unlock',
                '-n',
                self.name
            ]
            if self.uid is not None and info[2] != int(self.uid):
                cmd.append('-u')
                cmd.append(self.uid)
            return self.execute_command(cmd)
        return (rc, out, err)


class DragonFlyBsdUser(FreeBsdUser):
    """
    This is a DragonFlyBSD User manipulation class - it inherits the
    FreeBsdUser class behaviors, such as using the pw command to
    manipulate the user database, followed by the chpass command
    to change the password.
    """

    platform = 'DragonFly'


class OpenBSDUser(User):
    """
    This is a OpenBSD User manipulation class.
    Main differences are that OpenBSD:-
     - has no concept of "system" account.
     - has no force delete user

    This overrides the following methods from the generic class:-
      - create_user()
      - remove_user()
      - modify_user()
    """

    platform = 'OpenBSD'
    distribution = None
    SHADOWFILE = '/etc/master.passwd'

    def create_user(self):
        cmd = [self.module.get_bin_path('useradd', True)]

        if self.uid is not None:
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            cmd.append('-g')
            cmd.append(self.group)

        if self.groups is not None:
            groups = self.get_groups_set()
            cmd.append('-G')
            cmd.append(','.join(groups))

        if self.comment is not None:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.login_class is not None:
            cmd.append('-L')
            cmd.append(self.login_class)

        if self.password is not None and self.password != '*':
            cmd.append('-p')
            cmd.append(self.password)

        if self.create_home:
            cmd.append('-m')

            if self.skeleton is not None:
                cmd.append('-k')
                cmd.append(self.skeleton)

        cmd.append(self.name)
        return self.execute_command(cmd)

    def remove_user_userdel(self):
        cmd = [self.module.get_bin_path('userdel', True)]
        if self.remove:
            cmd.append('-r')
        cmd.append(self.name)
        return self.execute_command(cmd)

    def modify_user(self):
        cmd = [self.module.get_bin_path('usermod', True)]
        info = self.user_info()

        if self.uid is not None and info[2] != int(self.uid):
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            ginfo = self.group_info(self.group)
            if info[3] != ginfo[2]:
                cmd.append('-g')
                cmd.append(self.group)

        if self.groups is not None:
            current_groups = self.user_group_membership()
            groups_need_mod = False
            groups_option = '-S'
            groups = []

            if self.groups == '':
                if current_groups and not self.append:
                    groups_need_mod = True
            else:
                groups = self.get_groups_set()
                group_diff = set(current_groups).symmetric_difference(groups)

                if group_diff:
                    if self.append:
                        for g in groups:
                            if g in group_diff:
                                groups_option = '-G'
                                groups_need_mod = True
                                break
                    else:
                        groups_need_mod = True

            if groups_need_mod:
                cmd.append(groups_option)
                cmd.append(','.join(groups))

        if self.comment is not None and info[4] != self.comment:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None and info[5] != self.home:
            if self.move_home:
                cmd.append('-m')
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None and info[6] != self.shell:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.login_class is not None:
            # find current login class
            user_login_class = None
            userinfo_cmd = [self.module.get_bin_path('userinfo', True), self.name]
            (rc, out, err) = self.execute_command(userinfo_cmd, obey_checkmode=False)

            for line in out.splitlines():
                tokens = line.split()

                if tokens[0] == 'class' and len(tokens) == 2:
                    user_login_class = tokens[1]

            # act only if login_class change
            if self.login_class != user_login_class:
                cmd.append('-L')
                cmd.append(self.login_class)

        if self.update_password == 'always' and self.password is not None \
                and self.password != '*' and info[1] != self.password:
            cmd.append('-p')
            cmd.append(self.password)

        # skip if no changes to be made
        if len(cmd) == 1:
            return (None, '', '')

        cmd.append(self.name)
        return self.execute_command(cmd)


class NetBSDUser(User):
    """
    This is a NetBSD User manipulation class.
    Main differences are that NetBSD:-
     - has no concept of "system" account.
     - has no force delete user


    This overrides the following methods from the generic class:-
      - create_user()
      - remove_user()
      - modify_user()
    """

    platform = 'NetBSD'
    distribution = None
    SHADOWFILE = '/etc/master.passwd'

    def create_user(self):
        cmd = [self.module.get_bin_path('useradd', True)]

        if self.uid is not None:
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            cmd.append('-g')
            cmd.append(self.group)

        if self.groups is not None:
            groups = self.get_groups_set()
            if len(groups) > 16:
                self.module.fail_json(msg="Too many groups (%d) NetBSD allows for 16 max." % len(groups))
            cmd.append('-G')
            cmd.append(','.join(groups))

        if self.comment is not None:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.login_class is not None:
            cmd.append('-L')
            cmd.append(self.login_class)

        if self.password is not None:
            cmd.append('-p')
            cmd.append(self.password)

        if self.create_home:
            cmd.append('-m')

            if self.skeleton is not None:
                cmd.append('-k')
                cmd.append(self.skeleton)

        cmd.append(self.name)
        return self.execute_command(cmd)

    def remove_user_userdel(self):
        cmd = [self.module.get_bin_path('userdel', True)]
        if self.remove:
            cmd.append('-r')
        cmd.append(self.name)
        return self.execute_command(cmd)

    def modify_user(self):
        cmd = [self.module.get_bin_path('usermod', True)]
        info = self.user_info()

        if self.uid is not None and info[2] != int(self.uid):
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            ginfo = self.group_info(self.group)
            if info[3] != ginfo[2]:
                cmd.append('-g')
                cmd.append(self.group)

        if self.groups is not None:
            current_groups = self.user_group_membership()
            groups_need_mod = False
            groups = []

            if self.groups == '':
                if current_groups and not self.append:
                    groups_need_mod = True
            else:
                groups = self.get_groups_set()
                group_diff = set(current_groups).symmetric_difference(groups)

                if group_diff:
                    if self.append:
                        for g in groups:
                            if g in group_diff:
                                groups = set(current_groups).union(groups)
                                groups_need_mod = True
                                break
                    else:
                        groups_need_mod = True

            if groups_need_mod:
                if len(groups) > 16:
                    self.module.fail_json(msg="Too many groups (%d) NetBSD allows for 16 max." % len(groups))
                cmd.append('-G')
                cmd.append(','.join(groups))

        if self.comment is not None and info[4] != self.comment:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None and info[5] != self.home:
            if self.move_home:
                cmd.append('-m')
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None and info[6] != self.shell:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.login_class is not None:
            cmd.append('-L')
            cmd.append(self.login_class)

        if self.update_password == 'always' and self.password is not None and info[1] != self.password:
            cmd.append('-p')
            cmd.append(self.password)

        if self.password_lock:
            cmd.append('-C yes')
        elif self.password_lock is not None:
            cmd.append('-C no')

        # skip if no changes to be made
        if len(cmd) == 1:
            return (None, '', '')

        cmd.append(self.name)
        return self.execute_command(cmd)


class SunOS(User):
    """
    This is a SunOS User manipulation class - The main difference between
    this class and the generic user class is that Solaris-type distros
    don't support the concept of a "system" account and we need to
    edit the /etc/shadow file manually to set a password. (Ugh)

    This overrides the following methods from the generic class:-
      - create_user()
      - remove_user()
      - modify_user()
    """

    platform = 'SunOS'
    distribution = None
    SHADOWFILE = '/etc/shadow'

    def get_password_defaults(self):
        # Read password aging defaults
        try:
            minweeks = ''
            maxweeks = ''
            warnweeks = ''
            for line in open("/etc/default/passwd", 'r'):
                line = line.strip()
                if (line.startswith('#') or line == ''):
                    continue
                key, value = line.split('=')
                if key == "MINWEEKS":
                    minweeks = value.rstrip('\n')
                elif key == "MAXWEEKS":
                    maxweeks = value.rstrip('\n')
                elif key == "WARNWEEKS":
                    warnweeks = value.rstrip('\n')
        except Exception as err:
            self.module.fail_json(msg="failed to read /etc/default/passwd: %s" % to_native(err))

        return (minweeks, maxweeks, warnweeks)

    def remove_user(self):
        cmd = [self.module.get_bin_path('userdel', True)]
        if self.remove:
            cmd.append('-r')
        cmd.append(self.name)

        return self.execute_command(cmd)

    def create_user(self):
        cmd = [self.module.get_bin_path('useradd', True)]

        if self.uid is not None:
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            cmd.append('-g')
            cmd.append(self.group)

        if self.groups is not None:
            groups = self.get_groups_set()
            cmd.append('-G')
            cmd.append(','.join(groups))

        if self.comment is not None:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.create_home:
            cmd.append('-m')

            if self.skeleton is not None:
                cmd.append('-k')
                cmd.append(self.skeleton)

        cmd.append(self.name)

        (rc, out, err) = self.execute_command(cmd)
        if rc is not None and rc != 0:
            self.module.fail_json(name=self.name, msg=err, rc=rc)

        if not self.module.check_mode:
            # we have to set the password by editing the /etc/shadow file
            if self.password is not None:
                minweeks, maxweeks, warnweeks = self.get_password_defaults()
                try:
                    lines = []
                    for line in open(self.SHADOWFILE, 'rb').readlines():
                        line = to_native(line, errors='surrogate_or_strict')
                        fields = line.strip().split(':')
                        if not fields[0] == self.name:
                            lines.append(line)
                            continue
                        fields[1] = self.password
                        fields[2] = str(int(time.time() // 86400))
                        if minweeks:
                            fields[3] = str(int(minweeks) * 7)
                        if maxweeks:
                            fields[4] = str(int(maxweeks) * 7)
                        if warnweeks:
                            fields[5] = str(int(warnweeks) * 7)
                        line = ':'.join(fields)
                        lines.append('%s\n' % line)
                    open(self.SHADOWFILE, 'w+').writelines(lines)
                except Exception as err:
                    self.module.fail_json(msg="failed to update users password: %s" % to_native(err))

        return (rc, out, err)

    def modify_user_usermod(self):
        cmd = [self.module.get_bin_path('usermod', True)]
        cmd_len = len(cmd)
        info = self.user_info()

        if self.uid is not None and info[2] != int(self.uid):
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            ginfo = self.group_info(self.group)
            if info[3] != ginfo[2]:
                cmd.append('-g')
                cmd.append(self.group)

        if self.groups is not None:
            current_groups = self.user_group_membership()
            groups = self.get_groups_set()
            group_diff = set(current_groups).symmetric_difference(groups)
            groups_need_mod = False

            if group_diff:
                if self.append:
                    for g in groups:
                        if g in group_diff:
                            groups_need_mod = True
                            break
                else:
                    groups_need_mod = True

            if groups_need_mod:
                cmd.append('-G')
                new_groups = groups
                if self.append:
                    new_groups.update(current_groups)
                cmd.append(','.join(new_groups))

        if self.comment is not None and info[4] != self.comment:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None and info[5] != self.home:
            if self.move_home:
                cmd.append('-m')
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None and info[6] != self.shell:
            cmd.append('-s')
            cmd.append(self.shell)

        # modify the user if cmd will do anything
        if cmd_len != len(cmd):
            cmd.append(self.name)
            (rc, out, err) = self.execute_command(cmd)
            if rc is not None and rc != 0:
                self.module.fail_json(name=self.name, msg=err, rc=rc)
        else:
            (rc, out, err) = (None, '', '')

        # we have to set the password by editing the /etc/shadow file
        if self.update_password == 'always' and self.password is not None and info[1] != self.password:
            (rc, out, err) = (0, '', '')
            if not self.module.check_mode:
                minweeks, maxweeks, warnweeks = self.get_password_defaults()
                try:
                    lines = []
                    for line in open(self.SHADOWFILE, 'rb').readlines():
                        line = to_native(line, errors='surrogate_or_strict')
                        fields = line.strip().split(':')
                        if not fields[0] == self.name:
                            lines.append(line)
                            continue
                        fields[1] = self.password
                        fields[2] = str(int(time.time() // 86400))
                        if minweeks:
                            fields[3] = str(int(minweeks) * 7)
                        if maxweeks:
                            fields[4] = str(int(maxweeks) * 7)
                        if warnweeks:
                            fields[5] = str(int(warnweeks) * 7)
                        line = ':'.join(fields)
                        lines.append('%s\n' % line)
                    open(self.SHADOWFILE, 'w+').writelines(lines)
                    rc = 0
                except Exception as err:
                    self.module.fail_json(msg="failed to update users password: %s" % to_native(err))

        return (rc, out, err)


class DarwinUser(User):
    """
    This is a Darwin Mac OS X User manipulation class.
    Main differences are that Darwin:-
      - Handles accounts in a database managed by dscl(1)
      - Has no useradd/groupadd
      - Does not create home directories
      - User password must be cleartext
      - UID must be given
      - System users must ben under 500

    This overrides the following methods from the generic class:-
      - user_exists()
      - create_user()
      - remove_user()
      - modify_user()
    """
    platform = 'Darwin'
    distribution = None
    SHADOWFILE = None

    dscl_directory = '.'

    fields = [
        ('comment', 'RealName'),
        ('home', 'NFSHomeDirectory'),
        ('shell', 'UserShell'),
        ('uid', 'UniqueID'),
        ('group', 'PrimaryGroupID'),
        ('hidden', 'IsHidden'),
    ]

    def __init__(self, module):

        super(DarwinUser, self).__init__(module)

        # make the user hidden if option is set or deffer to system option
        if self.hidden is None:
            if self.system:
                self.hidden = 1
        elif self.hidden:
            self.hidden = 1
        else:
            self.hidden = 0

        # add hidden to processing if set
        if self.hidden is not None:
            self.fields.append(('hidden', 'IsHidden'))

    def _get_dscl(self):
        return [self.module.get_bin_path('dscl', True), self.dscl_directory]

    def _list_user_groups(self):
        cmd = self._get_dscl()
        cmd += ['-search', '/Groups', 'GroupMembership', self.name]
        (rc, out, err) = self.execute_command(cmd, obey_checkmode=False)
        groups = []
        for line in out.splitlines():
            if line.startswith(' ') or line.startswith(')'):
                continue
            groups.append(line.split()[0])
        return groups

    def _get_user_property(self, property):
        '''Return user PROPERTY as given my dscl(1) read or None if not found.'''
        cmd = self._get_dscl()
        cmd += ['-read', '/Users/%s' % self.name, property]
        (rc, out, err) = self.execute_command(cmd, obey_checkmode=False)
        if rc != 0:
            return None
        # from dscl(1)
        # if property contains embedded spaces, the list will instead be
        # displayed one entry per line, starting on the line after the key.
        lines = out.splitlines()
        # sys.stderr.write('*** |%s| %s -> %s\n' %  (property, out, lines))
        if len(lines) == 1:
            return lines[0].split(': ')[1]
        else:
            if len(lines) > 2:
                return '\n'.join([lines[1].strip()] + lines[2:])
            else:
                if len(lines) == 2:
                    return lines[1].strip()
                else:
                    return None

    def _get_next_uid(self, system=None):
        '''
        Return the next available uid. If system=True, then
        uid should be below of 500, if possible.
        '''
        cmd = self._get_dscl()
        cmd += ['-list', '/Users', 'UniqueID']
        (rc, out, err) = self.execute_command(cmd, obey_checkmode=False)
        if rc != 0:
            self.module.fail_json(
                msg="Unable to get the next available uid",
                rc=rc,
                out=out,
                err=err
            )

        max_uid = 0
        max_system_uid = 0
        for line in out.splitlines():
            current_uid = int(line.split(' ')[-1])
            if max_uid < current_uid:
                max_uid = current_uid
            if max_system_uid < current_uid and current_uid < 500:
                max_system_uid = current_uid

        if system and (0 < max_system_uid < 499):
            return max_system_uid + 1
        return max_uid + 1

    def _change_user_password(self):
        '''Change password for SELF.NAME against SELF.PASSWORD.

        Please note that password must be cleartext.
        '''
        # some documentation on how is stored passwords on OSX:
        # http://blog.lostpassword.com/2012/07/cracking-mac-os-x-lion-accounts-passwords/
        # http://null-byte.wonderhowto.com/how-to/hack-mac-os-x-lion-passwords-0130036/
        # http://pastebin.com/RYqxi7Ca
        # on OSX 10.8+ hash is SALTED-SHA512-PBKDF2
        # https://pythonhosted.org/passlib/lib/passlib.hash.pbkdf2_digest.html
        # https://gist.github.com/nueh/8252572
        cmd = self._get_dscl()
        if self.password:
            cmd += ['-passwd', '/Users/%s' % self.name, self.password]
        else:
            cmd += ['-create', '/Users/%s' % self.name, 'Password', '*']
        (rc, out, err) = self.execute_command(cmd)
        if rc != 0:
            self.module.fail_json(msg='Error when changing password', err=err, out=out, rc=rc)
        return (rc, out, err)

    def _make_group_numerical(self):
        '''Convert SELF.GROUP to is stringed numerical value suitable for dscl.'''
        if self.group is None:
            self.group = 'nogroup'
        try:
            self.group = grp.getgrnam(self.group).gr_gid
        except KeyError:
            self.module.fail_json(msg='Group "%s" not found. Try to create it first using "group" module.' % self.group)
        # We need to pass a string to dscl
        self.group = str(self.group)

    def __modify_group(self, group, action):
        '''Add or remove SELF.NAME to or from GROUP depending on ACTION.
        ACTION can be 'add' or 'remove' otherwise 'remove' is assumed. '''
        if action == 'add':
            option = '-a'
        else:
            option = '-d'
        cmd = ['dseditgroup', '-o', 'edit', option, self.name, '-t', 'user', group]
        (rc, out, err) = self.execute_command(cmd)
        if rc != 0:
            self.module.fail_json(msg='Cannot %s user "%s" to group "%s".'
                                      % (action, self.name, group), err=err, out=out, rc=rc)
        return (rc, out, err)

    def _modify_group(self):
        '''Add or remove SELF.NAME to or from GROUP depending on ACTION.
        ACTION can be 'add' or 'remove' otherwise 'remove' is assumed. '''

        rc = 0
        out = ''
        err = ''
        changed = False

        current = set(self._list_user_groups())
        if self.groups is not None:
            target = set(self.groups.split(','))
        else:
            target = set([])

        if self.append is False:
            for remove in current - target:
                (_rc, _err, _out) = self.__modify_group(remove, 'delete')
                rc += rc
                out += _out
                err += _err
                changed = True

        for add in target - current:
            (_rc, _err, _out) = self.__modify_group(add, 'add')
            rc += _rc
            out += _out
            err += _err
            changed = True

        return (rc, err, out, changed)

    def _update_system_user(self):
        '''Hide or show user on login window according SELF.SYSTEM.

        Returns 0 if a change has been made, None otherwise.'''

        plist_file = '/Library/Preferences/com.apple.loginwindow.plist'

        # http://support.apple.com/kb/HT5017?viewlocale=en_US
        cmd = ['defaults', 'read', plist_file, 'HiddenUsersList']
        (rc, out, err) = self.execute_command(cmd, obey_checkmode=False)
        # returned value is
        # (
        #   "_userA",
        #   "_UserB",
        #   userc
        # )
        hidden_users = []
        for x in out.splitlines()[1:-1]:
            try:
                x = x.split('"')[1]
            except IndexError:
                x = x.strip()
            hidden_users.append(x)

        if self.system:
            if self.name not in hidden_users:
                cmd = ['defaults', 'write', plist_file, 'HiddenUsersList', '-array-add', self.name]
                (rc, out, err) = self.execute_command(cmd)
                if rc != 0:
                    self.module.fail_json(msg='Cannot user "%s" to hidden user list.' % self.name, err=err, out=out, rc=rc)
                return 0
        else:
            if self.name in hidden_users:
                del (hidden_users[hidden_users.index(self.name)])

                cmd = ['defaults', 'write', plist_file, 'HiddenUsersList', '-array'] + hidden_users
                (rc, out, err) = self.execute_command(cmd)
                if rc != 0:
                    self.module.fail_json(msg='Cannot remove user "%s" from hidden user list.' % self.name, err=err, out=out, rc=rc)
                return 0

    def user_exists(self):
        '''Check is SELF.NAME is a known user on the system.'''
        cmd = self._get_dscl()
        cmd += ['-list', '/Users/%s' % self.name]
        (rc, out, err) = self.execute_command(cmd, obey_checkmode=False)
        return rc == 0

    def remove_user(self):
        '''Delete SELF.NAME. If SELF.FORCE is true, remove its home directory.'''
        info = self.user_info()

        cmd = self._get_dscl()
        cmd += ['-delete', '/Users/%s' % self.name]
        (rc, out, err) = self.execute_command(cmd)

        if rc != 0:
            self.module.fail_json(msg='Cannot delete user "%s".' % self.name, err=err, out=out, rc=rc)

        if self.force:
            if os.path.exists(info[5]):
                shutil.rmtree(info[5])
                out += "Removed %s" % info[5]

        return (rc, out, err)

    def create_user(self, command_name='dscl'):
        cmd = self._get_dscl()
        cmd += ['-create', '/Users/%s' % self.name]
        (rc, err, out) = self.execute_command(cmd)
        if rc != 0:
            self.module.fail_json(msg='Cannot create user "%s".' % self.name, err=err, out=out, rc=rc)

        self._make_group_numerical()
        if self.uid is None:
            self.uid = str(self._get_next_uid(self.system))

        # Homedir is not created by default
        if self.create_home:
            if self.home is None:
                self.home = '/Users/%s' % self.name
            if not self.module.check_mode:
                if not os.path.exists(self.home):
                    os.makedirs(self.home)
                self.chown_homedir(int(self.uid), int(self.group), self.home)

        # dscl sets shell to /usr/bin/false when UserShell is not specified
        # so set the shell to /bin/bash when the user is not a system user
        if not self.system and self.shell is None:
            self.shell = '/bin/bash'

        for field in self.fields:
            if field[0] in self.__dict__ and self.__dict__[field[0]]:

                cmd = self._get_dscl()
                cmd += ['-create', '/Users/%s' % self.name, field[1], self.__dict__[field[0]]]
                (rc, _err, _out) = self.execute_command(cmd)
                if rc != 0:
                    self.module.fail_json(msg='Cannot add property "%s" to user "%s".' % (field[0], self.name), err=err, out=out, rc=rc)

                out += _out
                err += _err
                if rc != 0:
                    return (rc, _err, _out)

        (rc, _err, _out) = self._change_user_password()
        out += _out
        err += _err

        self._update_system_user()
        # here we don't care about change status since it is a creation,
        # thus changed is always true.
        if self.groups:
            (rc, _out, _err, changed) = self._modify_group()
            out += _out
            err += _err
        return (rc, err, out)

    def modify_user(self):
        changed = None
        out = ''
        err = ''

        if self.group:
            self._make_group_numerical()

        for field in self.fields:
            if field[0] in self.__dict__ and self.__dict__[field[0]]:
                current = self._get_user_property(field[1])
                if current is None or current != self.__dict__[field[0]]:
                    cmd = self._get_dscl()
                    cmd += ['-create', '/Users/%s' % self.name, field[1], self.__dict__[field[0]]]
                    (rc, _err, _out) = self.execute_command(cmd)
                    if rc != 0:
                        self.module.fail_json(
                            msg='Cannot update property "%s" for user "%s".'
                                % (field[0], self.name), err=err, out=out, rc=rc)
                    changed = rc
                    out += _out
                    err += _err
        if self.update_password == 'always' and self.password is not None:
            (rc, _err, _out) = self._change_user_password()
            out += _out
            err += _err
            changed = rc

        if self.groups:
            (rc, _out, _err, _changed) = self._modify_group()
            out += _out
            err += _err

            if _changed is True:
                changed = rc

        rc = self._update_system_user()
        if rc == 0:
            changed = rc

        return (changed, out, err)


class AIX(User):
    """
    This is a AIX User manipulation class.

    This overrides the following methods from the generic class:-
      - create_user()
      - remove_user()
      - modify_user()
    """

    platform = 'AIX'
    distribution = None
    SHADOWFILE = '/etc/security/passwd'

    def remove_user(self):
        cmd = [self.module.get_bin_path('userdel', True)]
        if self.remove:
            cmd.append('-r')
        cmd.append(self.name)

        return self.execute_command(cmd)

    def create_user_useradd(self, command_name='useradd'):
        cmd = [self.module.get_bin_path(command_name, True)]

        if self.uid is not None:
            cmd.append('-u')
            cmd.append(self.uid)

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            cmd.append('-g')
            cmd.append(self.group)

        if self.groups is not None and len(self.groups):
            groups = self.get_groups_set()
            cmd.append('-G')
            cmd.append(','.join(groups))

        if self.comment is not None:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.create_home:
            cmd.append('-m')

            if self.skeleton is not None:
                cmd.append('-k')
                cmd.append(self.skeleton)

        cmd.append(self.name)
        (rc, out, err) = self.execute_command(cmd)

        # set password with chpasswd
        if self.password is not None:
            cmd = []
            cmd.append(self.module.get_bin_path('chpasswd', True))
            cmd.append('-e')
            cmd.append('-c')
            self.execute_command(cmd, data="%s:%s" % (self.name, self.password))

        return (rc, out, err)

    def modify_user_usermod(self):
        cmd = [self.module.get_bin_path('usermod', True)]
        info = self.user_info()

        if self.uid is not None and info[2] != int(self.uid):
            cmd.append('-u')
            cmd.append(self.uid)

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            ginfo = self.group_info(self.group)
            if info[3] != ginfo[2]:
                cmd.append('-g')
                cmd.append(self.group)

        if self.groups is not None:
            current_groups = self.user_group_membership()
            groups_need_mod = False
            groups = []

            if self.groups == '':
                if current_groups and not self.append:
                    groups_need_mod = True
            else:
                groups = self.get_groups_set()
                group_diff = set(current_groups).symmetric_difference(groups)

                if group_diff:
                    if self.append:
                        for g in groups:
                            if g in group_diff:
                                groups_need_mod = True
                                break
                    else:
                        groups_need_mod = True

            if groups_need_mod:
                cmd.append('-G')
                cmd.append(','.join(groups))

        if self.comment is not None and info[4] != self.comment:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None and info[5] != self.home:
            if self.move_home:
                cmd.append('-m')
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None and info[6] != self.shell:
            cmd.append('-s')
            cmd.append(self.shell)

        # skip if no changes to be made
        if len(cmd) == 1:
            (rc, out, err) = (None, '', '')
        else:
            cmd.append(self.name)
            (rc, out, err) = self.execute_command(cmd)

        # set password with chpasswd
        if self.update_password == 'always' and self.password is not None and info[1] != self.password:
            cmd = []
            cmd.append(self.module.get_bin_path('chpasswd', True))
            cmd.append('-e')
            cmd.append('-c')
            (rc2, out2, err2) = self.execute_command(cmd, data="%s:%s" % (self.name, self.password))
        else:
            (rc2, out2, err2) = (None, '', '')

        if rc is not None:
            return (rc, out + out2, err + err2)
        else:
            return (rc2, out + out2, err + err2)


class HPUX(User):
    """
    This is a HP-UX User manipulation class.

    This overrides the following methods from the generic class:-
      - create_user()
      - remove_user()
      - modify_user()
    """

    platform = 'HP-UX'
    distribution = None
    SHADOWFILE = '/etc/shadow'

    def create_user(self):
        cmd = ['/usr/sam/lbin/useradd.sam']

        if self.uid is not None:
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            cmd.append('-g')
            cmd.append(self.group)

        if self.groups is not None and len(self.groups):
            groups = self.get_groups_set()
            cmd.append('-G')
            cmd.append(','.join(groups))

        if self.comment is not None:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None:
            cmd.append('-d')
            cmd.append(self.home)

        if self.shell is not None:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.password is not None:
            cmd.append('-p')
            cmd.append(self.password)

        if self.create_home:
            cmd.append('-m')
        else:
            cmd.append('-M')

        if self.system:
            cmd.append('-r')

        cmd.append(self.name)
        return self.execute_command(cmd)

    def remove_user(self):
        cmd = ['/usr/sam/lbin/userdel.sam']
        if self.force:
            cmd.append('-F')
        if self.remove:
            cmd.append('-r')
        cmd.append(self.name)
        return self.execute_command(cmd)

    def modify_user(self):
        cmd = ['/usr/sam/lbin/usermod.sam']
        info = self.user_info()

        if self.uid is not None and info[2] != int(self.uid):
            cmd.append('-u')
            cmd.append(self.uid)

            if self.non_unique:
                cmd.append('-o')

        if self.group is not None:
            if not self.group_exists(self.group):
                self.module.fail_json(msg="Group %s does not exist" % self.group)
            ginfo = self.group_info(self.group)
            if info[3] != ginfo[2]:
                cmd.append('-g')
                cmd.append(self.group)

        if self.groups is not None:
            current_groups = self.user_group_membership()
            groups_need_mod = False
            groups = []

            if self.groups == '':
                if current_groups and not self.append:
                    groups_need_mod = True
            else:
                groups = self.get_groups_set(remove_existing=False)
                group_diff = set(current_groups).symmetric_difference(groups)

                if group_diff:
                    if self.append:
                        for g in groups:
                            if g in group_diff:
                                groups_need_mod = True
                                break
                    else:
                        groups_need_mod = True

            if groups_need_mod:
                cmd.append('-G')
                new_groups = groups
                if self.append:
                    new_groups = groups | set(current_groups)
                cmd.append(','.join(new_groups))

        if self.comment is not None and info[4] != self.comment:
            cmd.append('-c')
            cmd.append(self.comment)

        if self.home is not None and info[5] != self.home:
            cmd.append('-d')
            cmd.append(self.home)
            if self.move_home:
                cmd.append('-m')

        if self.shell is not None and info[6] != self.shell:
            cmd.append('-s')
            cmd.append(self.shell)

        if self.update_password == 'always' and self.password is not None and info[1] != self.password:
            cmd.append('-F')
            cmd.append('-p')
            cmd.append(self.password)

        # skip if no changes to be made
        if len(cmd) == 1:
            return (None, '', '')

        cmd.append(self.name)
        return self.execute_command(cmd)


def main():
    ssh_defaults = dict(
        bits=0,
        type='rsa',
        passphrase=None,
        comment='ansible-generated on %s' % socket.gethostname()
    )
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=['absent', 'present']),
            name=dict(type='str', required=True, aliases=['user']),
            uid=dict(type='str'),
            non_unique=dict(type='bool', default=False),
            group=dict(type='str'),
            groups=dict(type='list'),
            comment=dict(type='str'),
            home=dict(type='path'),
            shell=dict(type='str'),
            password=dict(type='str', no_log=True),
            login_class=dict(type='str'),
            # following options are specific to macOS
            hidden=dict(type='bool'),
            # following options are specific to selinux
            seuser=dict(type='str'),
            # following options are specific to userdel
            force=dict(type='bool', default=False),
            remove=dict(type='bool', default=False),
            # following options are specific to useradd
            create_home=dict(type='bool', default=True, aliases=['createhome']),
            skeleton=dict(type='str'),
            system=dict(type='bool', default=False),
            # following options are specific to usermod
            move_home=dict(type='bool', default=False),
            append=dict(type='bool', default=False),
            # following are specific to ssh key generation
            generate_ssh_key=dict(type='bool'),
            ssh_key_bits=dict(type='int', default=ssh_defaults['bits']),
            ssh_key_type=dict(type='str', default=ssh_defaults['type']),
            ssh_key_file=dict(type='path'),
            ssh_key_comment=dict(type='str', default=ssh_defaults['comment']),
            ssh_key_passphrase=dict(type='str', no_log=True),
            update_password=dict(type='str', default='always', choices=['always', 'on_create']),
            expires=dict(type='float'),
            password_lock=dict(type='bool'),
            local=dict(type='bool'),
        ),
        supports_check_mode=True
    )

    user = User(module)

    module.debug('User instantiated - platform %s' % user.platform)
    if user.distribution:
        module.debug('User instantiated - distribution %s' % user.distribution)

    rc = None
    out = ''
    err = ''
    result = {}
    result['name'] = user.name
    result['state'] = user.state
    if user.state == 'absent':
        if user.user_exists():
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = user.remove_user()
            if rc != 0:
                module.fail_json(name=user.name, msg=err, rc=rc)
            result['force'] = user.force
            result['remove'] = user.remove
    elif user.state == 'present':
        if not user.user_exists():
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = user.create_user()
            if module.check_mode:
                result['system'] = user.name
            else:
                result['system'] = user.system
                result['create_home'] = user.create_home
        else:
            # modify user (note: this function is check mode aware)
            (rc, out, err) = user.modify_user()
            result['append'] = user.append
            result['move_home'] = user.move_home
        if rc is not None and rc != 0:
            module.fail_json(name=user.name, msg=err, rc=rc)
        if user.password is not None:
            result['password'] = 'NOT_LOGGING_PASSWORD'

    if rc is None:
        result['changed'] = False
    else:
        result['changed'] = True
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    if user.user_exists():
        info = user.user_info()
        if info is False:
            result['msg'] = "failed to look up user name: %s" % user.name
            result['failed'] = True
        result['uid'] = info[2]
        result['group'] = info[3]
        result['comment'] = info[4]
        result['home'] = info[5]
        result['shell'] = info[6]
        if user.groups is not None:
            result['groups'] = user.groups

        # handle missing homedirs
        info = user.user_info()
        if user.home is None:
            user.home = info[5]
        if not os.path.exists(user.home) and user.create_home:
            if not module.check_mode:
                user.create_homedir(user.home)
                user.chown_homedir(info[2], info[3], user.home)
            result['changed'] = True

        # deal with ssh key
        if user.sshkeygen:
            # generate ssh key (note: this function is check mode aware)
            (rc, out, err) = user.ssh_key_gen()
            if rc is not None and rc != 0:
                module.fail_json(name=user.name, msg=err, rc=rc)
            if rc == 0:
                result['changed'] = True
            (rc, out, err) = user.ssh_key_fingerprint()
            if rc == 0:
                result['ssh_fingerprint'] = out.strip()
            else:
                result['ssh_fingerprint'] = err.strip()
            result['ssh_key_file'] = user.get_ssh_key_path()
            result['ssh_public_key'] = user.get_ssh_public_key()

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
