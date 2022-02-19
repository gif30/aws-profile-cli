import typer
from typing import Optional
import configparser
import os
import json
from subprocess import check_output, CalledProcessError
import re
import sys


def get_profiles() -> list[str]:
    profiles_cmd = "aws configure list-profiles"
    out = check_output(profiles_cmd, shell=True).decode(sys.stdout.encoding)
    profiles = out.split()
    return profiles


def completion_profiles(incomplete: str)-> list[str]:
    completion = []
    profiles = get_profiles()
    for profile in profiles:
        
        if profile.startswith((incomplete)):
            completion.append(profile)
    return completion


app = typer.Typer()



@app.command()
def test(name: Optional[str] = None):
    print_actual_profile()
    print_aws_get_caller_identity()


if __name__ == "__main__":
    app()


@app.command()
def switch(profile: str = typer.Argument(default=...,autocompletion=completion_profiles)):
    profiles = get_profiles()
    if profile in profiles:
        typer.echo(f"Setting {profile} as default")
        try:
            set_aws_default_profile(profile)

        except Exception as e:
            typer.echo('Failed to set profile: ' + str(e), err=True)
            exit(1)
        typer.echo('funciono todo piola')
        print_aws_get_caller_identity()

    else:
        typer.echo(f'profile "{profile}" not configured', err=True)



#AWS

# get last 4 bytes of access key and secret key from aws-cli
def get_profile_key_endings(profile):
    command = "aws configure list --profile {profile}".format(profile=profile)
    
    try:
        output = check_output(command, shell=True)
        t = 0, output
    except CalledProcessError as e:
        t = e.returncode, e.message
        #print(t)
        raise ValueError(t)
    
    # filter command
    regex_access_key = re.compile(r"(?:access_key\ +\*+)([A-Za-z0-9]+)")
    regex_secret_key = re.compile(r"(?:secret_key\ +\*+)([A-Za-z0-9]+)")
    access_key_ending = regex_access_key.search(str(output)).group(1)
    secret_key_ending = regex_secret_key.search(str(output)).group(1)
    # print(access_key_ending)
    # print(secret_key_ending)
    
    return access_key_ending, secret_key_ending


def get_profile_credentials_from_cache(profile):
    access_key_ending, secret_key_ending = get_profile_key_endings(profile)
    
    cache_cli_path = os.path.join(os.path.expanduser('~'), '.aws/cli/cache')
    json_files = [pos_json for pos_json in os.listdir(
        cache_cli_path) if pos_json.endswith('.json')]
    # print(json_files)  # for me this prints ['foo.json']
    
    for file in json_files:
        file = os.path.join(cache_cli_path, file)
        with open(file, 'r') as a_file:
            a_json = json.load(a_file)
            #pretty_json = json.dumps(a_json, indent=4)
            # print(pretty_json)
            creds = a_json["Credentials"]
            if a_json["ProviderType"] == 'sso' and creds["AccessKeyId"][-4:] == access_key_ending and creds["SecretAccessKey"][-4:] == secret_key_ending:
        
                if creds["AccessKeyId"] and creds["SecretAccessKey"] and creds["SessionToken"] and creds["Expiration"]:
                    pass
                else:
                    raise ValueError("error, no pude obtener las credenciales nuevas")
    
                return creds


def set_default_profile_credentials(aws_access_key, aws_secret_key, aws_session_token, aws_expiration, aws_profile):
    credentials_path = os.path.join(
        os.path.expanduser('~'), '.aws/credentials')
    config = configparser.ConfigParser()
    config.read(credentials_path)
    # print(config.sections())
    
    config['default'] = {
        'aws_access_key_id': aws_access_key,
        'aws_secret_access_key': aws_secret_key,
        'profile': aws_profile
    }
    if aws_session_token:
        config['default']['aws_session_token'] = aws_session_token
    if aws_expiration:
        config['default']['expiry_date'] = aws_expiration
    with open(credentials_path, 'w') as configfile:
        config.write(configfile)


def set_aws_default_profile(profile):

    typer.echo('wtf')

    if aws_profile_is_sso(profile):
        creds = get_profile_credentials_from_cache(profile)
        aws_profile = profile
        aws_access_key = creds["AccessKeyId"]
        aws_secret_key = creds["SecretAccessKey"]
        aws_session_token = creds["SessionToken"]
        aws_expiration = creds["Expiration"]


    else: 
        creds = get_profile_credentials_from_credsfile(profile)
        aws_profile = profile
        aws_access_key = creds["aws_access_key_id"]
        aws_secret_key = creds["aws_secret_access_key"]
        aws_session_token = None
        aws_expiration = None


    # set credentials file
    set_default_profile_credentials(aws_access_key, aws_secret_key, aws_session_token, aws_expiration, aws_profile)

def print_aws_get_caller_identity():
    profiles_cmd = "aws sts get-caller-identity"
    out = check_output(profiles_cmd, shell=True).decode(sys.stdout.encoding)
    typer.echo(out)

def print_actual_profile():
    profiles_cmd = "aws configure get profile"
    out = check_output(profiles_cmd, shell=True).decode(sys.stdout.encoding)
    typer.echo(out)

def aws_profile_is_sso(profile) -> bool:

    config_path = os.path.join(
        os.path.expanduser('~'), '.aws/config')
    config = configparser.ConfigParser()
    config.read(config_path)
    # print(config.sections())

    if config[profile]['sso_start_url']:
        return True
    else:
        return False

def get_profile_credentials_from_credsfile(profile):
    credentials_path = os.path.join(
        os.path.expanduser('~'), '.aws/credentials')
    config = configparser.ConfigParser()
    config.read(credentials_path)
    # print(config.sections())
    

    creds = config[profile]
    creds['profile'] = profile
    return creds
