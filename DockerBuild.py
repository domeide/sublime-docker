import User.dockerutils
import sublime, sublime_plugin
import os

class DockerBuildCommand(sublime_plugin.WindowCommand):

    type = "RUN"
    docker_image = "python"
    docker_image_tag = "2.7xx" # Value seems to be unused?
    docker_image_exe = "python"

    def run(self, type="RUN", docker_image="python", docker_image_tag="2.7", docker_image_exe="python", file_regex='UNSET'):
        self.type = type
        self.docker_image = docker_image
        self.docker_image_tag = docker_image_tag
        self.docker_image_exe = docker_image_exe
        self.file_regex = file_regex
        self.file_name = User.dockerutils.getFileName()
        self.file_dir = User.dockerutils.getFileDir()
        
        if not User.dockerutils.isDockerRunning():
            """
               DISABLING status_message as this is not intrusive enough
               in the case that docker daemon is not installed/running
               sublime.status_message("It seems Docker is not installed on your machine. Try https://get.docker.com/")
            """
            sublime.error_message("Docker is not running on your machine, do you need to install it? Try https://get.docker.com/")
        elif User.dockerutils.isUnsupportedFileType(self.file_name):
            sublime.status_message("Cannot " + type.lower() + " an unsupported file type")
        else:
            self.executeFile()


    def executeFile(self):
        if self.type == "RUN":
            opt_volume =  " -v " + self.file_dir+"/:/src"
            opt_temporary = " -t"
            opt_cleanup = " --rm"
            image = " " + self.docker_image + ":" + self.docker_image_tag
            build_cmd =  " " + self.docker_image_exe + " /src/"+self.file_name
            command = ["docker run" + opt_volume + opt_temporary + opt_cleanup + image + build_cmd]
        else:
            self.errorMessage("Unknown command: " + self.type)
            return

        User.dockerutils.getView().window().run_command("exec", { 'kill': True })
        User.dockerutils.getView().window().run_command("exec", {
            'shell': True,
            'cmd': command,
            'working_dir' : self.file_dir,
            'file_regex'  : self.file_regex
        })

    
