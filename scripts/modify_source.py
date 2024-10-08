import fileinput
import os
import shutil
import subprocess

ENGINE_DIR = os.getenv('ENGINE_DIR', os.getcwd())
print(f'ENGINE_DIR: {ENGINE_DIR}')


def DeleteLineIfTextInLine(filePath, text):
    if not os.path.exists(filePath):
        filePath = os.path.join(ENGINE_DIR, filePath)
    for line in fileinput.input(filePath, inplace=True):
        if text not in line:
            print(line, end='')


def ReplaceText(filePath, oldText, newText):
    if not os.path.exists(filePath):
        filePath = os.path.join(ENGINE_DIR, filePath)
    with open(filePath, 'r', encoding='utf-8') as f:
        filedata = f.read()
        filedata = filedata.replace(oldText, newText)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(filedata)


def ReplaceTextInMultiFiles(filePaths, oldText, newText):
    for filePath in filePaths:
        ReplaceText(filePath, oldText, newText)


def ReplaceTextBySearchFile(fileName, oldText, newText):
    filePaths = ExecShell(f'find . -name {fileName}', ENGINE_DIR).splitlines()
    print(f'search {fileName} results: {filePaths}')
    ReplaceTextInMultiFiles(filePaths, oldText, newText)


def AppendNewLineAfter(filePath, text, appendText):
    ReplaceText(filePath, text, f'{text}\n{appendText}\n')


def InsertNewLineBefore(filePath, text, insertText):
    ReplaceText(filePath, text, f'\n{insertText}\n{text}')


def AppendNewLineAfterIfTextInLine(filePath, text, appendText):
    if not os.path.exists(filePath):
        filePath = os.path.join(ENGINE_DIR, filePath)
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(filePath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            if text in line:
                f.write(f'{appendText}\n')


def InsertNewLineBeforeIfTextInLine(filePath, text, insertText):
    if not os.path.exists(filePath):
        filePath = os.path.join(ENGINE_DIR, filePath)
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(filePath, 'w', encoding='utf-8') as f:
        for line in lines:
            if text in line:
                f.write(f'{insertText}\n')
            f.write(line)


def ExecShell(command, directory):
    result = subprocess.run(command, cwd=directory, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.stdout


def RemoveUnitTest():
    print(f'remove unittest')
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
        DeleteLineIfTextInLine("src/flutter/BUILD.gn", text)


def FixSnapshotHash(snapshotHash=None):
    if snapshotHash is None:
        snapshotHash = ExecShell(
            'python3 tools/make_version.py --format {{SNAPSHOT_HASH}}', os.path.join(ENGINE_DIR, 'src/third_party/dart')
        )

    print(f'fix snapshot_hash to {snapshotHash}')
    ReplaceText(
        'src/third_party/dart/tools/make_version.py',
        'snapshot_hash = MakeSnapshotHashString()',
        f'snapshot_hash = "{snapshotHash}"',
    )


def DisableVerifyCert():
    print(f'disable verify cert')
    AppendNewLineAfterIfTextInLine(
        'src/flutter/third_party/boringssl/src/ssl/ssl_x509.cc',
        'STACK_OF(X509) *const cert_chain = session->x509_chain;',
        '  return true;',
    )


def SetTcpSocketProxy(ipStr, port):
    print(f'set tcp socket proxy to {ipStr}:{port}')
    InsertNewLineBeforeIfTextInLine(
        'src/third_party/dart/runtime/bin/socket.cc',
        'SocketAddress::SetAddrPort(&addr, static_cast<intptr_t>(port));',
        f'''
  Syslog::PrintErr("ref: %s",inet_ntoa(addr.in.sin_addr));
  if(port>50){{
      port={port};
      addr.addr.sa_family=AF_INET;
      addr.in.sin_family=AF_INET;
      inet_aton("{ipStr}", &addr.in.sin_addr);
  }}
''',
    )


def ReplaceModifyFiles(srcDir, dstDir):
    shutil.copytree(srcDir, dstDir, dirs_exist_ok=True)


def ModifyService():
    print(f'modify service')

    # dark sdk 的 dart 代码是在 Dark VM 中运行的，flutter build 时会被 AOT 编译进 libapp.so，不在 libflutter.so 中，所以修改dart代码不会生效


def main():
    RemoveUnitTest()
    FixSnapshotHash()
    DisableVerifyCert()

    ModifyService()


if __name__ == '__main__':
    print('py modify source start')
    main()
    print('py modify source finish')
