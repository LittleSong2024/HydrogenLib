import os
import platform
import re
import sys

from subprocess import run, PIPE
from argparse import ArgumentParser


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
        if not tag.startswith('v-'):  # 保证 v-patch-... 等标签不被误伤
            tag = tag.removeprefix('v')
        return tag


class TagChecker:
    # on:
    #     push:
    #         tags:
    #             - "v*.*.*-upload*"
    #             - "v-patch-upload*"
    #             - "v-major-upload*"
    #             - "v-minor-upload*"
    def __init__(self):
        self.re_v_vvv = re.compile(r'v(\d+\.\d+\.\d+)-upload.*')
        self.re_v_patch = re.compile(r'v-(patch)-upload.*')
        self.re_v_major = re.compile(r'v-(major)-upload.*')
        self.re_v_minor = re.compile(r'v-(minor)-upload.*')

        self.re_ls = [
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

    def load_version(self):
        ps = run(['hatch', 'version'], stdout=PIPE)
        version = ps.stdout.decode('utf-8').strip()
        print("Version:", repr(version))
        self.version = version

    def check_tag(self):
        tag = self.parser.get_tag_name()
        if tag:
            # 解析标签
            curv = self.checker.match(tag)
            libv = self.version
            # 如果传入的标签版本号小于当前版本号，则不执行上传
            if curv not in {'patch', 'major', 'minor'} and tuple(curv.split('.')) < tuple(libv.split('.')):
                print('当前版本号大于传入的版本号，不执行上传')
                sys.exit(1)  # 阻止工作流继续执行

            print('更新版本号:', curv)
            self.update_version(curv)

    def update_version(self, ver):
        run(['hatch', 'version', ver])

    def upload(self):
        run(['twine', 'upload', './dist/*'])

    def build(self):
        run(['hatch', 'build'])

    def exec(self):

        print(f'Upload script runs on {platform.platform()}')
        print(f'PID: {os.getpid()}')
        print(f'Args: {sys.argv}')
        print(f'Env: {os.environ}')

        self.load_version()

        print(f'Get-Version: {self.version}')

        self.check_tag()
        self.build()
        self.upload()


if __name__ == '__main__':
    main = Main()
    main.exec()
