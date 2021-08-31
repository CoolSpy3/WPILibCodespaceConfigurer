import os
import re
import shutil
import sys

# Credit: https://stackoverflow.com/questions/2656322/shutil-rmtree-fails-on-windows-with-access-is-denied Justin Peel
def onrmerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onrmerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

args = sys.argv
args.pop(0)

if len(args) < 1:
	print("No Projects Specified")
	exit()

if "-h" in args or "--help" in args:
	print("Usage: configure.py [-u <name>] [repos]")
	exit(0)

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
pathPattern = re.compile(re.escape("path = ") + r'([^\s]+)')

oldDir = os.getcwd()

try:

	dir = os.path.dirname(os.path.abspath(__file__))

	devcontainerconfig = None

	with open(os.path.join(dir, "config", "devcontainer.json"), "r") as file:
		devcontainerconfig = file.readlines()

	for repo in args:
		os.chdir(dir)
		match = repoPattern.match(repo)
		if not match:
			print(f'Invalid Repo: {repo}')
			continue
		name = match.group(1)
		try:
			os.system(f'git clone {repo}')
			shutil.rmtree(os.path.join(dir, name, ".devcontainer"), ignore_errors=True)
			postCreateCommand = ""
			submodulesPath = os.path.join(dir, name, ".gitmodules")
			if(os.path.exists(submodulesPath)):
				postCreateCommand = '"postCreateCommand": "'
				with open(submodulesPath, "r") as submodulesFile:
					for line in submodulesFile.readlines():
						pathMatch = pathPattern.search(line)
						if pathMatch:
							postCreateCommand += f'rm -rf {pathMatch.group(1)} & '
				postCreateCommand += 'git submodule update --init",'
			devcontainer = os.path.join(dir, name, ".devcontainer")
			os.mkdir(devcontainer)
			shutil.copy(os.path.join(dir, "config", "Dockerfile"), devcontainer)
			newdevcontainerconfig = [(line, f'\t{postCreateCommand}')[re.sub("[^a-zA-Z0-9" + re.escape("{}") + "]", "", line) == "{{postCreateCommand}}"] for line in devcontainerconfig]
			with open(os.path.join(devcontainer, "devcontainer.json"), "w") as devcontainerconfigfile:
				devcontainerconfigfile.writelines(newdevcontainerconfig)
			#os.system(f'cp -r {os.path.join(os.getcwd(), "config", profile)}/. {os.path.join(os.getcwd(), name)}/')
			os.chdir(name)
			#os.system("git add .")
			#os.system('git commit -m "support codespaces"')
			#os.system('git push')
		finally:
			os.chdir(dir)
			shutil.rmtree(os.path.join(dir, name), onerror=onrmerror)

finally:
	os.chdir(oldDir)
