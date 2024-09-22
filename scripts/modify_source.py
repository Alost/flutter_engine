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

def ReplaceFileText(filePath, oldText, newText):
    if not os.path.exists(filePath):
        filePath = os.path.join(ENGINE_DIR, filePath)
    with open(filePath, 'r', encoding='utf-8') as f:
        filedata = f.read()
        filedata = filedata.replace(oldText, newText)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(filedata)

def RemoveUnitTest():
    texts = [
        # android 的单元测试
        "//flutter/impeller/toolkit/android:apk_unittests",
        "//flutter/impeller/toolkit/android:unittests",
        "//flutter/shell/platform/android:flutter_shell_native_unittests",
        # impeller 的单元测试
        "//flutter/impeller:impeller_dart_unittests",
        "//flutter/impeller:impeller_unittests",
        "//flutter/impeller/toolkit/interop:example",
        # mobile 的单元测试
        "//flutter/shell/platform/android/external_view_embedder:android_external_view_embedder_unittests",
        "//flutter/shell/platform/android/jni:jni_unittests",
        "//flutter/shell/platform/android/platform_view_android_delegate:platform_view_android_delegate_unittests",
    ]
    for text in texts:
        DeleteFileTextLine("src/flutter/BUILD.gn", text)



def main():
    RemoveUnitTest()


if __name__ == '__main__':
    main()
    print('modify source done')
