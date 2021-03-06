from waflib import Utils

def __get_cc_env_vars__(cc):
    cmd = cc + ['-dM', '-E', '-']
    try:
        p = Utils.subprocess.Popen(cmd, stdin=Utils.subprocess.PIPE,
                                        stdout=Utils.subprocess.PIPE,
                                        stderr=Utils.subprocess.PIPE)
        p.stdin.write('\n'.encode())
        return p.communicate()[0]
    except Exception:
        return ""

def __test_and_add_flags__(ctx, flags):
    for flag in flags:
        ctx.check_cc(cflags=flag, uselib_store="compiler", mandatory=False)
    ctx.env.CFLAGS += ctx.env.CFLAGS_compiler

def __add_generic_flags__(ctx):
    ctx.env.CFLAGS += ["-D_ISOC99_SOURCE", "-D_GNU_SOURCE",
                       "-D_LARGEFILE_SOURCE", "-D_FILE_OFFSET_BITS=64",
                       "-D_LARGEFILE64_SOURCE",
                       "-std=c99", "-Wall"]

    if ctx.is_debug_build():
        ctx.env.CFLAGS += ['-g']

def __add_gcc_flags__(ctx):
    ctx.env.CFLAGS += ["-Wall", "-Wundef", "-Wmissing-prototypes", "-Wshadow",
                       "-Wno-switch", "-Wno-parentheses", "-Wpointer-arith",
                       "-Wredundant-decls", "-Wno-pointer-sign",
                       "-Werror=implicit-function-declaration",
                       "-Wno-error=deprecated-declarations",
                       "-Wno-error=unused-function" ]
    __test_and_add_flags__(ctx, ["-Wempty-body"])
    __test_and_add_flags__(ctx, ["-Wdisabled-optimization"])
    __test_and_add_flags__(ctx, ["-Wstrict-prototypes"])

def __add_clang_flags__(ctx):
    ctx.env.CFLAGS += ["-Wno-logical-op-parentheses", "-fcolor-diagnostics",
                       "-Wno-tautological-compare",
                       "-Wno-tautological-constant-out-of-range-compare" ]

def __add_mingw_flags__(ctx):
    ctx.env.CFLAGS += ['-D__USE_MINGW_ANSI_STDIO=1']
    ctx.env.CFLAGS += ['-DBYTE_ORDER=1234']
    ctx.env.CFLAGS += ['-DLITLE_ENDIAN=1234']
    ctx.env.CFLAGS += ['-DBIG_ENDIAN=4321']
    ctx.env.LAST_LINKFLAGS += ['-mwindows']

def __add_cygwin_flags__(ctx):
    ctx.env.CFLAGS += ['-mwin32']
    ctx.env.CFLAGS += ['-U__STRICT_ANSI__']

__compiler_map__ = {
    '__GNUC__':  __add_gcc_flags__,
    '__clang__': __add_clang_flags__,
    '__MINGW32__': __add_mingw_flags__,
    '__CYGWIN__': __add_cygwin_flags__,
}

def __apply_map__(ctx, fnmap):
    if not getattr(ctx, 'CC_ENV_VARS', None):
        ctx.CC_ENV_VARS = str(__get_cc_env_vars__(ctx.env.CC))
    for k, fn in fnmap.items():
        if ctx.CC_ENV_VARS.find(k) > 0:
            fn(ctx)

def configure(ctx):
    __add_generic_flags__(ctx)
    __apply_map__(ctx, __compiler_map__)

