# !/usr/bin/env python3

import os
import subprocess

data = {
    k.removeprefix('GIT_PUSH_'): v
    for k, v in os.environ.items()
    if k.startswith('GIT_PUSH_OPTION_')
}


if __name__ == '__main__':
    if "no-verify" not in data.values():
        subprocess.run(['git', 'push', 'origin', '--tags', '--push-option=no-verify'])
