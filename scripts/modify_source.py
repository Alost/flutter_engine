import fileinput
import os
import shutil

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


def ModifySnapshotHash(snapshotHash):
    print(f'modify snapshot_hash to {snapshotHash}')
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
    ReplaceText(
        'src/third_party/dart/sdk/lib/convert/json.dart',
        'dynamic convert(String input) => _parseJson(input, _reviver);',
        '''
    dynamic convert(String input) {
        var result = _parseJson(input, _reviver);
        if (result is Map<String, dynamic>) {
            if (result.containsKey('data') && result['data'] is Map<String, dynamic>) {
                if result['data'].containsKey('trialVip') {
                    print("get user info");
                    final vipTime = "2024-01-01 00:00:00";
                    final svipTime = "2024-02-01 00:00:00";
                    result['data']['trialVip'] = 0;
                    result['data']['vipTime'] = vipTime;
                    result['data']['maColorKlineDeadline'] = vipTime;
                    result['data']['svipTime'] = svipTime;
                    result['data']['pureSvipTime'] = svipTime;
                } else if (result['data'].containsKey('androidDownloadUrl')) {
                    print("get version info");
                }
            }
        }
        return result;
    }
''',
    )

    ReplaceText(
        'src/third_party/dart/sdk/lib/_http/http_impl.dart',
        '''
  Future<HttpClientRequest> openUrl(String method, Uri url) =>
      _openUrl(method, url);
''',
        '''
    Future<HttpClientRequest> openUrl(String method, Uri url) async {
        print("open url, method=$method, url=${url.path}");
    return _openUrl(method, url);
    }
''',
    )


def main():
    RemoveUnitTest()

    snapshotHash = 'd20a1be77c3d3c41b2a5accaee1ce549'

    ModifySnapshotHash(snapshotHash)
    DisableVerifyCert()

    ModifyService()


if __name__ == '__main__':
    print('py modify source start')
    main()
    print('py modify source finish')
