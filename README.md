# aws profile tools
to switch easily


## instalation
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