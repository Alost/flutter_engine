import fileinput
import os
import shutil

ENGINE_DIR = os.getenv('ENGINE_DIR', os.getcwd())
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


def AppendNewLineAfterText(filePath, text, lineText):
    ReplaceFileText(filePath, text, f'{text}\n{lineText}\n')


def AppendNewLineAfterTextInLine(filePath, text, lineText):
    if not os.path.exists(filePath):
        filePath = os.path.join(ENGINE_DIR, filePath)
    with open(filePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(filePath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            if text in line:
                f.write(f'{lineText}\n')


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


def ModifySnapshotHash(snapshotHash):
    ReplaceFileText(
        'src/third_party/dart/tools/make_version.py',
        'snapshot_hash = MakeSnapshotHashString()',
        f'snapshot_hash = "{snapshotHash}"',
    )


def DisableVerifyCert():
    AppendNewLineAfterTextInLine(
        'src/flutter/third_party/boringssl/src/ssl/ssl_x509.cc',
        'STACK_OF(X509) *const cert_chain = session->x509_chain;',
        'return true;',
    )


def ReplaceModifyFiles(srcDir, dstDir):
    shutil.copytree(srcDir, dstDir, dirs_exist_ok=True)


def main():
    RemoveUnitTest()

    snapshotHash = 'd20a1be77c3d3c41b2a5accaee1ce549'

    ModifySnapshotHash('snapshotHash')
    DisableVerifyCert()

    ReplaceFileText(
        'src/third_party/dart/tools/sdks/dart-sdk/lib/convert/json.dart',
        'dynamic convert(String input) => _parseJson(input, _reviver);',
        '''
    dynamic convert(String input) {
        var result = _parseJson(input, _reviver);
        if (result is Map<String, dynamic>) {
            if (result.containsKey('data') && result['data'] is Map<String, dynamic>) {
                if result['data'].containsKey('trialVip') {
                    print("get user info");
                    final vipTime = "2025-10-05 00:00:00";
                    final svipTime = "2025-10-05 00:00:00";
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

#     ReplaceFileText(
#         'src/third_party/dart/sdk/lib/_http/http_impl.dart',
#         '',
#         '''
# ''',
#     )


if __name__ == '__main__':
    print('py modify source start')
    main()
    print('py modify source finish')
