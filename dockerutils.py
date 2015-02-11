import sublime, sublime_plugin
import os, re, subprocess

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
    if len(os.popen("ps -aef | grep '/bin/docker ' | grep -v grep").read().strip()) < 1:
        return False
    return True

def isDockerRunningOnOSX():
    if len(os.popen("ps -aef | grep 'boot2docker' | grep -v grep").read().strip()) < 1:
        return False
    try:
        os.environ["DOCKER_HOST"]
        os.environ["DOCKER_CERT_PATH"]
        os.environ["DOCKER_TLS_VERIFY"]
    except KeyError:
        shellinit = subprocess.check_output(["/usr/local/bin/boot2docker", "shellinit"], stderr=None).strip()
        env = dict(re.findall(r'(\S+)=(".*?"|\S+)', shellinit.decode()))
        for key,value in env.items():
            os.environ[key]=value
    return True

def isNotRunningMessage():
    platform = sublime.platform()
    if platform == 'linux':
        isNotRunningMessageLinux()
    if platform == 'osx':
        isNotRunningMessageOSX()

def isNotRunningMessageLinux():
    sublime.error_message("Docker is not running on your machine, do you need to install it? Try https://get.docker.com/")        

def isNotRunningMessageOSX():
    sublime.error_message("On OSX platform, environment variables\n" +
        "\tDOCKER_HOST\n\tDOCKER_CERT_PATH\n\tDOCKER_TLS_VERIFY\n" + 
        "should be set in order to run Docker client")

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


