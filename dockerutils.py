import sublime, sublime_plugin
import os, re, subprocess
import time, shutil
import os.path

opt_cleanup = '--rm'

# Used by logDockerCommand(command) below:
#SUBLIME_DOCKER_LOGFILE='/tmp/sublime-docker.log'
SUBLIME_DOCKER_LOGFILE=None

DOCKER_NOT_INSTALLED_LINUX_MSG='''Docker is not installed. 

Install it to use SublimeDocker: open a Terminal and run
    'curl -sSL https://get.docker.com/ | sh'
'''

DOCKER_NOT_INSTALLED_OSX_MSG='''Docker is not installed. 

Install it to use SublimeDocker. Visit the following URL for installation instructions:

    https://docs.docker.com/en/latest/installation/
'''

DOCKER_NOT_RUNNING_LINUX_MSG='''Docker engine is not running. 

Start it to use SublimeDocker.
'''
DOCKER_NOT_RUNNING_OSX_MSG='''Docker engine is not running. 

Start it to use SublimeDocker: open a Terminal and run 'docker-machine start $(docker-machine active)' or 'boot2docker up'
'''

def isDockerInstalled():
    platform = sublime.platform()
    if platform == 'linux':
        return isDockerInstalledOnLinux()
    if platform == 'osx':
        return isDockerInstalledOnOSX()

def isDockerRunning():
    platform = sublime.platform()
    if platform == 'linux':
        return isDockerRunningOnLinux()
    if platform == 'osx':
        return isDockerRunningOnOSX()

def isDockerRunningOnLinux():
    """ Check is Docker daemon is running:
          We assume that the path to the daemon which appears in full ps output
          is of the form */bin/docker
    """
    if len(os.popen("ps -aef | grep '/bin/docker ' | grep -v grep").read().strip()) > 0:
        return True
    if len(os.popen("ps -aef | grep '/bin/docker.io ' | grep -v grep").read().strip()) > 0:
        return True
    return False

def isDockerRunningOnOSX():
    return (
        (os.path.isfile('/usr/local/bin/boot2docker')  
            and isBoot2DockerRunning()) or
        (os.path.isfile('/usr/local/bin/docker-machine')  
            and isDockerMachineRunning()))
    

def isBoot2DockerRunning():
    if len(os.popen("ps -aef | grep 'boot2docker' | grep -v grep").read().strip()) < 1:
        return False
    try:
        os.environ["DOCKER_HOST"]
        os.environ["DOCKER_CERT_PATH"]
        os.environ["DOCKER_TLS_VERIFY"]
    except KeyError:
        boot2docker_init_cmd = subprocess.check_output(["/usr/local/bin/boot2docker", "shellinit"], stderr=None).strip()
        env = dict(re.findall(r'(\S+)=(".*?"|\S+)', boot2docker_init_cmd.decode()))
        for key,value in env.items():
            os.environ[key]=value
    return True

def isDockerMachineRunning():
    machine_ls = os.popen("/usr/local/bin/docker-machine ls -q").read().strip()
    if len(machine_ls) < 1:
        return False
    try:
        os.environ["DOCKER_HOST"]
        os.environ["DOCKER_CERT_PATH"]
        os.environ["DOCKER_TLS_VERIFY"]
        os.environ["DOCKER_MACHINE_NAME"]
    except KeyError:
        home_dir = os.path.expanduser('~')
        dockermachine_init_cmd = subprocess.check_output(
            "docker-machine -s " + home_dir + "/.docker/machine env default; exit 0", 
            stderr=subprocess.STDOUT, shell=True, env={"PATH": "/usr/local/bin"}).decode()
        env = dict(re.findall(r'(\S+)=(".*?"|\S+)', dockermachine_init_cmd))
        for key,value in env.items():
            os.environ[key]=value.strip('"')
    return True

def isDockerInstalledOnLinux():
    if shutil.which('docker') != None :
        return True
    return False

def isDockerInsalledOnOSX():
    if shutil.which('docker') == None:
        return False
    if (shutil.which('boot2docker') == None
        and shutil.which('docker-machine') == None) :
        return False
    return True

def isNotRunningMessage():
    platform = sublime.platform()
    if platform == 'linux':
        isNotRunningMessageLinux()
    if platform == 'osx':
        isNotRunningMessageOSX()

def isNotInstalledMessageLinux():
    sublime.error_message(DOCKER_NOT_INSTALLED_LINUX_MSG)

def isNotInstalledMessageOSX():
    sublime.error_message(DOCKER_NOT_INSTALLED_OSX_MSG)

def isNotRunningMessageLinux():
    sublime.error_message(DOCKER_NOT_RUNNING_LINUX_MSG)        

def isNotRunningMessageOSX():
    sublime.error_message(DOCKER_NOT_RUNNING_OSX_MSG)

def isUnsupportedFileType(file_name):
    return False

def getFileFullPath():
    win = sublime.active_window()
    if win:
        view = win.active_view()
        if view and view.file_name():
            return view.file_name()
    return ""

def getFileDir():
    filefullpath = getFileFullPath()
    dirname = os.path.dirname(filefullpath)
    if os.path.exists(dirname):
        return dirname
    else:
        return ""

def getFileName():
    filefullpath = getFileFullPath()
    return os.path.basename(filefullpath)

def getView():
    win = sublime.active_window()
    return win.active_view()

def getCommand():
    platform = sublime.platform()
    if platform == 'linux':
        return "docker"
    if platform == 'osx':
        return "/usr/local/bin/docker"

def logDockerCommand(command):
    if SUBLIME_DOCKER_LOGFILE != None:
        with open(SUBLIME_DOCKER_LOGFILE, 'a+') as f:
            f.write(time.strftime("\n%d/%m/%Y %H:%M:%S ") + str(command))
            f.close()

