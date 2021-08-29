import os
import re
import sys

args = sys.argv
args.pop(0)

if len(args) < 1:
	print("No Projects Specified")
	exit()

if args[0].lower() == "-u":
	args.pop(0)
	user = args[0]
	args.pop(0)
	if(user.endswith('/')):
		user = user[:-1]
	args = [f'{user}/{repo}' for repo in args]

if len(args) < 1:
        print("No Projects Specified")
        exit()

args = [f'https://github.com/{repo}' for repo in args]

repoPattern = re.compile(re.escape('https://github.com/') + r'(?:[a-zA-Z0-9_-]+)\/([a-zA-Z0-9_-]+)(?:.git)?')

oldDir = os.getcwd()

try:

	dir = os.path.dirname(os.path.abspath(__file__))

	for repo in args:
		os.chdir(dir)
		match = repoPattern.match(repo)
		if not match:
			print("invalid repo")
		name = match.group(1)
		try:
			os.system(f'git clone --recurse-submodules {repo}')
			hasLib199 = os.path.exists(os.path.join(os.getcwd(), f'{name}', "lib199"))
			profile = "default"
			if hasLib199:
				profile = "lib199"
			os.system(f'cp -r {os.path.join(os.getcwd(), "config", profile)}/. {os.path.join(os.getcwd(), name)}/')
			os.chdir(name)
			os.system("git add .")
			os.system('git commit -m "support codespaces"')
			os.system('git push')
		finally:
			os.chdir(dir)
			os.system(f'rm -rf {name}')

finally:
	os.chdir(oldDir)
