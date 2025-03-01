from .pyd.bitmap import *


if __name__ == '__main__':
    bp = Bitmap(10)
    for i in range(0, 10*8, 10):
        bp.set(i, True)

    for i in range(0, 10*8, 10):
        print(bp.get(i))

