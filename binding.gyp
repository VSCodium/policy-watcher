{
    "targets": [
        {
            "target_name": "vscodium-policy-watcher",
            "sources": [
                "src/main.cc"
            ],
            "include_dirs": [
                "<!(node -p \"require('node-addon-api').include_dir\")"
            ],
            "defines": [ "NODE_API_SWALLOW_UNTHROWABLE_EXCEPTIONS", "NAPI_CPP_EXCEPTIONS" ],
            "cflags!": [
                "-fno-exceptions"
            ],
            "cflags_cc!": [
                "-fno-exceptions"
            ],
            'conditions': [
                ['OS=="mac"', {
                    "sources": [
                        "src/macos/PolicyWatcher.cc",
                        "src/macos/StringPolicy.cc",
                        "src/macos/NumberPolicy.cc",
                        "src/macos/BooleanPolicy.cc",
                        "src/macos/UnionPolicy.cc"
                    ],
                    "defines": [
                        "MACOS",
                    ],
                    "xcode_settings": {
                        "MACOSX_DEPLOYMENT_TARGET": "10.13",
                        "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
                        "CLANG_CXX_LIBRARY": "libc++"
                    },
                    "variables": {
                        "cxx": "clang++"
                    },
                    "cflags!": [
                        "-mmacosx-version-min=10.7"
                    ],
                    "cflags": [
                        "-O2", "-fstack-protector-strong", "-mmacosx-version-min=10.13"
                    ],
                    "cflags_cc": [
                        "-mmacosx-version-min=10.13"
                    ]
                }],
                ['OS=="mac" and target_arch=="arm64"', {
                    "xcode_settings": {
                        "ARCHS": ["arm64"]
                    }
                }],
                ['OS=="linux"', {
                    "sources": [
                        "src/linux/PolicyWatcher.cc",
                    ],
                    "defines": [
                        "LINUX",
                    ],
                    "cflags": [
                        "-O2", "-fstack-protector-strong"
                    ]
                }],
                ["OS=='win'", {
                    "sources": [
                        "src/windows/PolicyWatcher.cc",
                        "src/windows/StringPolicy.cc",
                        "src/windows/NumberPolicy.cc",
                        "src/windows/BooleanPolicy.cc",
                        "src/windows/UnionPolicy.cc"
                    ],
                    "defines": [
                        "WINDOWS"
                    ],
                    "libraries": [
                        "-luserenv.lib"
                    ],
                    "msvs_configuration_attributes": {
                        "SpectreMitigation": "Spectre"
                    },
                    "msvs_settings": {
                        "VCCLCompilerTool": {
                            "ExceptionHandling": 1,
                            'AdditionalOptions': [
                                '/guard:cf',
                                '/W3',
                                '/we4146',
                                '/we4244',
                                '/we4267',
                                '/sdl',
                                '/ZH:SHA_256'
                            ],
                        },
                        'VCLinkerTool': {
                            'AdditionalOptions': [
                                '/DYNAMICBASE',
                                '/guard:cf'
                            ]
                        }
                    },
                }],
            ],
        }
    ]
}
