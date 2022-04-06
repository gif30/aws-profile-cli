from subprocess import check_output, CalledProcessError

profiles_cmd = "aws configure list-profiles"
out = check_output(profiles_cmd, shell=True)
print(out)
possible_choices = out.split()
print(possible_choices)
