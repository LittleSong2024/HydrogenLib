import os
import platform
import re
import sys

from subprocess import run as _run, PIPE


def run(*args, **kwargs):
    if kwargs.get('check') is None:
        kwargs['check'] = True
    return _run(*args, **kwargs)


class TagChecker:
    # on:
    #     push:
    #         tags:
    #             - "v-current-upload*"
    #             - "v*.*.*-upload*"
    #             - "v-patch-upload*"
    #             - "v-major-upload*"
    #             - "v-minor-upload*"
    def __init__(self):
        self.re_v_current = re.compile(r'v-(current)-upload.*')
        self.re_v_vvv = re.compile(r'v(\d+\.\d+\.\d+)-upload.*')
        self.re_v_patch = re.compile(r'v-(patch)-upload.*')
        self.re_v_major = re.compile(r'v-(major)-upload.*')
        self.re_v_minor = re.compile(r'v-(minor)-upload.*')

        self.re_ls = [
            self.re_v_current,
            self.re_v_vvv,
            self.re_v_patch,
            self.re_v_major,
            self.re_v_minor,
        ]

    def match(self, tag):
        for re in self.re_ls:
            res = re.match(tag)
            if res:
                return res.group(1)
        return None


class Main:
    def __init__(self):
        self.checker = TagChecker()
        self.version = None
        self.tag = None

    def load_version(self):
        ps = run(['hatch', 'version'], stdout=PIPE)
        version = ps.stdout.decode('utf-8').strip()
        print("Version:", repr(version))
        self.version = version

    def check_tag(self, tag):
        if tag:
            # 解析标签
            curv = self.checker.match(tag)
            if not curv:
                raise ValueError(f'无法解析标签版本号: {tag}')
            libv = self.version
            # 如果传入的标签版本号小于当前版本号，则不执行上传
            if curv not in {'patch', 'major', 'minor', 'current'} and tuple(curv.split('.')) < tuple(libv.split('.')):
                print('当前版本号大于传入的版本号，不执行上传')
                sys.exit(1)  # 阻止工作流继续执行
            if curv == 'current':
                print('不更新版本号')
            else:
                print('更新版本号:', curv)
                self.set_version(curv)

    def set_version(self, ver):
        run(['hatch', 'version', ver])

    def upload(self):
        run(['twine', 'upload', './dist/*'])

    def build(self):
        run(['hatch', 'build'])

    def show_info(self):
        print(f'Upload script runs on {platform.platform()}')
        print(f'PID: {os.getpid()}')
        print(f'Args: {sys.argv}')
        print(f'Activity tag: {self.tag}')
        print(f'Get-Library-Version: {self.version}')

    def exec(self):
        self.load_version()
        self.show_info()

        self.check_tag(os.environ.get('TAG'))
        self.build()
        self.upload()


if __name__ == '__main__':
    main = Main()
    main.exec()
