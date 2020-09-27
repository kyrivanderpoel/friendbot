from setuptools import setup

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
    name="friendbot",
    version="0.1",
    py_modules=["friendbot"],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        friendbot-cli=friendbot.cli:cli
    """,
)
