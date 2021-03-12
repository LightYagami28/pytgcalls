import os
import site
import time

from setuptools import setup
from setuptools.command.install import install


class PostInstall(install):
    @staticmethod
    def get_version(package_check) -> dict:
        result_cmd = os.popen(f'{package_check} -v').read()
        result_cmd = result_cmd.replace('v', '')
        if len(result_cmd) == 0:
            return {
                'version_int': 0,
                'version': '0',
            }
        return {
            'version_int': int(result_cmd.split('.')[0]),
            'version': result_cmd,
        }

    # noinspection PyBroadException
    def run(self):
        install.run(self)
        node_result = self.get_version('node')
        npm_result = self.get_version('npm')
        if node_result['version_int'] == 0:
            raise Exception('Please install node (15.+)')
        if npm_result['version_int'] == 0:
            raise Exception('Please install npm (7.+)')
        if node_result['version_int'] < 15:
            raise Exception(
                'Needed node 15.+, '
                'actually installed is '
                f"{node_result['version']}",
            )
        if npm_result['version_int'] < 7:
            raise Exception(
                'Needed npm 7.+, '
                'actually installed is '
                f"{npm_result['version']}",
            )
        os.system('npm install')
        os.system('npm install --prefix pytgcalls/js/')
        time.sleep(1.0)


setup(
    cmdclass={
        'install': PostInstall,
    },
)
if 'pip' in os.getcwd():
    os.system(
        'cp -r '
        f'{os.getcwd()}/pytgcalls/js/lib '
        f'{site.getsitepackages()[0]}/pytgcalls/js/',
    )
    os.system(
        'cp -r '
        'pytgcalls/js/node_modules '
        f'{site.getsitepackages()[0]}/pytgcalls/js/',
    )