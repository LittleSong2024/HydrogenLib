import platform

if platform.system() == 'Windows':
    from .windows import *

if platform.system() == 'Linux':
    from .linux import *
