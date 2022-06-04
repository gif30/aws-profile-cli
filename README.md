# aws profile tools
to switch easily

## Requirements
python 3.10 or above
python -m pip install typer-cli
python -m pip install poetry

## instalation
### Easy install:
```
bash install.sh
```
### Manual install:
https://typer.tiangolo.com/tutorial/package/
```
poetry build
pip install --user dist/aws_profile-0.1.0-py3-none-any.whl
aws-profile --install-completion
```

## Generate docs
```
typer aws_profile.main utils docs --output README-cli.md
```


# TODO
- packetize with environment (para no pisar paquetes de python locales)