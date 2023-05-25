from distutils.core import setup

setup(
    name="frchat",
    version="0.1.0",
    description="",
    author="wangyan",
    py_modules=[
        'fr_python_sdk.frrpc',
        'frchat.bot',
        'frchat.gui',
        'frchat.bot_palletize',
        'frchat.init_prompt_palletize',
        'frchat.init_prompt_rbtcmd',
        'frmovewrapper.frmove',
        'frmovewrapper.robotmath'
    ]
)