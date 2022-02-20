from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ck-widgets-lv",
    version="0.2",
    description="Unofficial Textual List View for Widgets that supports scrolling. Short and dirty hack to use while waiting for official ListView.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Cvaniak",
    author_email="igna.cwaniak@gmail.com",
    # packages=["ck_widgets_lv"],
    py_modules=['ck_widgets_lv'],
    scripts=['ck_widgets_lv.py'],
    install_requires=["rich", "textual"],
    zip_safe=False,
)
