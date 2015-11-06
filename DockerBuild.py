from . import dockerutils
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
        self.file_name = dockerutils.getFileName()
        self.file_dir = dockerutils.getFileDir()
    
        if not dockerutils.isDockerInstalled:
            dockerutils.isNotInstalledMessage()
        elif not dockerutils.isDockerRunning():
            dockerutils.isNotRunningMessage()
        elif dockerutils.isUnsupportedFileType(self.file_name):
            sublime.status_message("Cannot " + type.lower() + " an unsupported file type")
        else:
            self.executeFile()


    def executeFile(self):
        if self.type == "RUN":
            opt_volume =  " -v \"" + self.file_dir+"/\":/src"
            opt_temporary = " -t"
            image = " " + self.docker_image + ":" + self.docker_image_tag
            docker_cmd = dockerutils.getCommand()
            build_cmd = self.generateBuildCmd()
            command = [docker_cmd + " run" + opt_volume + opt_temporary + ' ' + dockerutils.opt_cleanup + image + build_cmd]
            dockerutils.logDockerCommand(command)
        else:
            self.errorMessage("Unknown command: " + self.type)
            return

        dockerutils.getView().window().run_command("exec", { 'kill': True })
        dockerutils.getView().window().run_command("exec", {
            'shell': True,
            'cmd': command,
            'working_dir' : self.file_dir,
            'file_regex'  : self.file_regex
        })

    
    def generateBuildCmd(self):
        cpp_check_list = ["gcc", "g++", "cpp", "c++"]
        exec_cmd = ""
        if any(map(lambda x: x in self.docker_image or x in self.docker_image_exe, cpp_check_list)):
            exec_cmd = "./a.out;"
        build_cmd =  " " + self.docker_image_exe + " \"/src/" + self.file_name + "\"; "
        build_cmd = " bash -c 'cd /src; " + build_cmd + exec_cmd + "'"
        return build_cmd