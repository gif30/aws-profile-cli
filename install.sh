#!/bin/bash
typer aws_profile.main utils docs --output README-cli.md
poetry build
pip install --user dist/aws_profile-0.1.0-py3-none-any.whl --force-reinstall
aws-profile --install-completion
