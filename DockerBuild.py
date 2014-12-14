import sublime, sublime_plugin
import os

def isDockerMissing():
    return False

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


class DockerBuildCommand(sublime_plugin.WindowCommand):

    type = "RUN"
    docker_image = "python"
    docker_image_tag = "2.7"
    docker_image_exe = "python"

    def run(self, type="RUN", docker_image="python", docker_image_tag="2.7", docker_image_exe="python"):
        self.type = type
        self.docker_image = docker_image
        self.docker_image_tag = docker_image_tag
        self.docker_image_exe = docker_image_exe
        self.file_name = getFileName()
        self.file_dir = getFileDir()
        
        if isDockerMissing():
            sublime.status_message("It seems Docker is not installed on your machine. Try https://get.docker.com/")
        elif isUnsupportedFileType(self.file_name):
            sublime.status_message("Cannot " + type.lower() + " an unsupported file type")
        else:
            self.executeFile()


    def executeFile(self):
        if self.type == "RUN":
            opt_volume =  " -v " + self.file_dir+"/:/src"
            opt_temporary = " -t"
            image = " " + self.docker_image + ":" + self.docker_image_tag
            build_cmd =  " " + self.docker_image_exe + " /src/"+self.file_name
            command = ["docker run" + opt_volume + opt_temporary + image + build_cmd]
        else:
            self.errorMessage("Unknown command: " + self.type)
            return

        getView().window().run_command("exec", { 'kill': True })
        getView().window().run_command("exec", {
            'shell': True,
            'cmd': command,
            'working_dir' : self.file_dir
        })

    