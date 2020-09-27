from setuptools import setup


setup(
    name="friendbot",
    version="0.1",
    py_modules=["friendbot"],
    entry_points="""
        [console_scripts]
        friendbot-cli=friendbot.cli:cli
    """,
)
