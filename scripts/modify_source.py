import fileinput
import os

ENGINE_DIR = os.getcwd()
print(f'ENGINE_DIR: {ENGINE_DIR}')


def DeleteFileTextLine(filePath, text):
    if not os.path.exists(filePath):
        filePath = os.path.join(ENGINE_DIR, filePath)
    for line in fileinput.input(filePath, inplace=True):
        if text not in line:
            print(line, end='')

def RemoveAndroidUnitTest():
    # 去掉 android 的单元测试
    texts = [
      "//flutter/impeller/toolkit/android:apk_unittests",
      "//flutter/impeller/toolkit/android:unittests",
      "//flutter/shell/platform/android:flutter_shell_native_unittests",
    ]
    for text in texts:
        DeleteFileTextLine("src/flutter/BUILD.gn", text)


def main():
    RemoveAndroidUnitTest()


if __name__ == '__main__':
    main()
    print('modify source done')
