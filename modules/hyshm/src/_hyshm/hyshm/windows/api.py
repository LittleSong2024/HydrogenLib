from _hyctypes import *

# 注册函数
# CreateFileMapping
# MapViewOfFile
# UnmapViewOfFile
# CopyMemory
# CloseHandle

kernel32 = HyDll('kernel32.dll')


@kernel32.define
def CreateFileMapping(
        hFile: c_int, lpFileMappingAttributes: c_void_p,
        flProtect: c_int, dwMaximumSizeHigh: c_int, dwMaximumSizeLow: c_int,
        lpName: c_char_p) -> c_void_p: ...
