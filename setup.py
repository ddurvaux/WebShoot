from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('./payload.py', base=base)
]

setup(name='WebShoot',
      version = '1.0',
      description = 'Take Screenshot of website',
      options = dict(build_exe = buildOptions),
      executables = executables)
