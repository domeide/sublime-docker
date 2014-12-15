import sublime, sublime_plugin
import os, re

def isDockerRunning():
    """ Check is Docker daemon is running:
          We assume that the path to the daemon which appears in full ps output
          is of the form */bin/docker
    """
    if len(os.popen("ps -aef | grep '/bin/docker ' | grep -v grep").read().strip()) < 1:
        return False
    return True

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


class DockerClojureBuildCommand(sublime_plugin.WindowCommand):

    type = "RUN"
    docker_image = "clojure"
    docker_image_tag = "2.5.0"
    docker_image_exe = "lein run"

    def run(self, type="RUN", docker_image="clojure", docker_image_tag="2.5.0", docker_image_exe="lein run", file_regex='UNSET'):
        self.type = type
        self.docker_image = docker_image
        self.docker_image_tag = docker_image_tag
        self.docker_image_exe = docker_image_exe
        self.file_regex = file_regex
        self.file_name = getFileName()
        self.file_dir = getFileDir()
        components = self.file_dir.split(os.sep)
        self.project_dir = str.join(os.sep, components[:components.index("src")])
        self.file_dir_relative_to_project = str.join(os.sep, components[components.index("src"):])
        self.file_dir_relative_to_src = str.join(os.sep, components[components.index("src")+1:])
        
        if not isDockerRunning():
            """
               DISABLING status_message as this is not intrusive enough
               in the case that docker daemon is not installed/running
               sublime.status_message("It seems Docker is not installed on your machine. Try https://get.docker.com/")
            """
            sublime.error_message("Docker is not running on your machine, do you need to install it? Try https://get.docker.com/")
        elif isUnsupportedFileType(self.file_name):
            sublime.status_message("Cannot " + type.lower() + " an unsupported file type")
        else:
            self.executeFile()


    def executeFile(self):
        if self.type == "RUN":
            opt_volume =  " -v " + self.project_dir+"/:/leinproject"
            opt_temporary = " -t"
            opt_cleanup = " --rm"
            opt_working_dir = " -w=\""+ "/leinproject/" + "\""
            image = " " + self.docker_image + ":" + self.docker_image_tag
            build_cmd =  " " + self.docker_image_exe
            command = ["docker run" + opt_volume + opt_temporary + opt_cleanup + opt_working_dir + image + build_cmd]
        else:
            self.errorMessage("Unknown command: " + self.type)
            return

        getView().window().run_command("exec", { 'kill': True })
        getView().window().run_command("exec", {
            'shell': True,
            'cmd': command,
            'working_dir' : self.file_dir,
            'file_regex'  : self.file_regex
        })

    
