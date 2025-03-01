import os
import shutil
from pathlib import Path
from subprocess import call


def main():
    cwd = Path(__file__).parent
    os.chdir(cwd)

    print('Building...')
    call(['python', 'setup.py', 'build'])

    build_dir = cwd / 'build'
    # lib_dir = list(build_dir.glob('lib*'))[0]
    # ls = list(lib_dir.glob('hybitmap*.pyd'))

    ls = list(build_dir.glob('**/hybitmap*.pyd'))
    file = ls[0] if len(ls) == 1 else None  # type: Path

    if file is None:
        print('No file found')
        return

    print('Copy file...')
    pyd_file_name = (cwd / 'pyd' / file.name)
    pyd_file_name.unlink(True)
    try:
        shutil.copy2(file, pyd_file_name)
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f'Failed to copy file({e})')
        return
    except Exception as e:
        print('Failed to copy file({e)')
        return

    print('Clean up...')
    shutil.rmtree(build_dir)


if __name__ == '__main__':
    main()
