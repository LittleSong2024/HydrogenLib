import argparse
import os
import subprocess
import sys
import time

import rich.traceback
from rich import print

rich.traceback.install()


def run_command(command):
    ps = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ps.returncode, ps


def init_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--install", '-i',
        help="Install HydrogenLib",
        action="store_true"
    )
    parser.add_argument(
        "--skip-check", '-c',
        help="Skip check HydrogenLib wheel",
        action="store_true"
    )
    parser.add_argument(
        "--skip-upload", '-d',
        help="Skip upload HydrogenLib wheel",
        action="store_true"
    )
    parser.add_argument(
        '--skip-build', '-s',
        help="Skip building HydrogenLib wheel",
        action="store_true"
    )
    parser.add_argument(
        "--clean", '-k',
        help="Clean HydrogenLib wheel",
        action="store_true"
    )
    parser.add_argument(  # 接收一个参数，version
        "--version", '-v',
        help="Set HydrogenLib version",
        default="None",
        type=str
    )


def pre_check():
    code, ps = run_command(['pip', 'install', '-U', 'twine', 'hatch'])
    if code != 0:
        console.print("[bold red]Installing dependencies failed!")
        console.print(ps.stderr.decode())
        sys.exit(code)


version_path = r"src/hydrolib/src\version"
spinner = "aesthetic"
args = sys.argv[1::]

if __name__ == '__main__':
    pre_check()

    parser = argparse.ArgumentParser()
    console = rich.console.Console(force_terminal=True)
    init_parser(parser)
    args = parser.parse_args(args)
    if args.version != "None":
        with console.status("Setting version...", spinner=spinner):
            rt_code, ps = run_command(["hatch", "version", args.version])
        time.sleep(0.1)
        if rt_code != 0:
            console.print("[bold red]Setting version failed!")
            console.print(ps.stderr.decode())
            console.print(ps.stdout.decode())
            sys.exit(rt_code)
        print("[bold green]success!")
    if args.clean:
        if os.name == 'nt':
            command = ["powershell.exe", "-Command", "rm", r".\dist\*"]
        elif os.name == 'posix':
            command = ["rm", "-rf", r"./dist/*"]
        else:
            console.print(f"[bold red]Unsupported OS({os.name})!")
            sys.exit(1)

        with console.status("Cleaning old files...", spinner=spinner):
            rt_code, ps = run_command(command)
        time.sleep(0.1)
        if rt_code != 0:
            console.print("[bold red]Cleaning old files failed!")
            console.print(ps.stderr.decode())
            console.print(ps.stdout.decode())
            sys.exit(rt_code)
        print("[bold green]success!")

    if not args.skip_build:
        # 播放工作动画
        with console.status("Building wheel...", spinner=spinner):
            rt_code, ps = run_command(["hatch", "build"])
        time.sleep(0.1)
        if rt_code != 0:
            console.print("[bold red]Building wheel failed!")
            console.print(ps.stderr.decode())
            sys.exit(rt_code)
        print("[bold green]success!")
    # console.console.print('\n')
    if not args.skip_check:
        with console.status("Checking wheel...", spinner=spinner):
            rt_code, ps = run_command(["twine", "check", "dist/*"])
        time.sleep(0.1)
        if rt_code != 0:
            console.print("[bold red]Checking wheel failed!")
            console.print(ps.stdout)
            console.print(ps.stderr)
            sys.exit(rt_code)
        print("[bold green]success!")
    # console.console.print('\n')
    if not args.skip_upload:
        print('Upload...')
        # ps = subprocess.run(["twine", "upload", r".\dist\*", '--disable-progress-bar'])
        ps = subprocess.run(["twine", "upload", r".\dist\*"])
        rt_code = ps.returncode
        if rt_code != 0:
            console.print(f"[bold red]failed!({rt_code})")
            console.print(ps.stdout.decode())
            console.print(ps.stderr.decode())
            sys.exit(rt_code)
        print("[bold green]success!")

    print(
        "[green]All steps are success, "
        "you can run "
        "[/green]`[#FFA500]pip[/#FFA500] install [blue]HydrogenLib[#FFA500]-[/#FFA500]Next[/blue] "
        "[dim]-U[/dim]` "
        "[green]to update HydrogenLib.")
