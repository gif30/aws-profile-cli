from setuptools import setup

setup(
    name='aws-switch-profile',
    version='0.1',
    py_modules=['aws_switch_profile'],
    install_requires=[
        'Click',
	"click_completion"
    ],
    entry_points='''
        [console_scripts]
        aws-switch-profile=aws_switch_profile:set_aws_default
    ''',
)
