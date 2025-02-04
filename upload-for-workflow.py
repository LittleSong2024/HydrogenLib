import os
import platform
import re
import sys

from subprocess import run as _run, PIPE
from argparse import ArgumentParser


def run(*args, **kwargs):
    if kwargs.get('check') is None:
        kwargs['check'] = True
    return _run(*args, **kwargs)


class MyParser(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument(
            '--tag', '-t',
            type=str,
            help='tag name',
            required=True
        )

    def get_tag_name(self, args=None):
        if args is None:
            args = sys.argv[1:]

        nsp = self.parse_args(args)
        tag = nsp.tag.removeprefix('refs/tags/')
        return tag


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
        self.parser = MyParser()
        self.checker = TagChecker()
        self.version = None
        self.tag = None

    def load_version(self):
        ps = run(['hatch', 'version'], stdout=PIPE)
        version = ps.stdout.decode('utf-8').strip()
        print("Version:", repr(version))
        self.version = version

    def check_tag(self):
        self.tag = tag = self.parser.get_tag_name()
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
                self.update_version(curv)

    def update_version(self, ver):
        run(['hatch', 'version', ver])

    def upload(self):
        run(['twine', 'upload', './dist/*'])

    def build(self):
        run(['hatch', 'build'])

    def exec(self):

        self.load_version()

        print(f'Upload script runs on {platform.platform()}')
        print(f'PID: {os.getpid()}')
        print(f'Args: {sys.argv}')
        print(f'Env: {os.environ}')
        print(f'Activity tag: {self.parser.get_tag_name()}')
        print(f'Get-Version: {self.version}')

        self.check_tag()
        self.build()
        self.upload()


if __name__ == '__main__':
    main = Main()
    main.exec()
