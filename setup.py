from distutils.core import setup

setup(
    name="frchat",
    version="0.1.0",
    description="",
    author="wangyan",
    py_modules=[
        'fr_python_sdk.frrpc',
        'frchat.*',
        'frmovewrapper.*',
    ]
)