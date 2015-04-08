from . import dockerutils
import sublime, sublime_plugin
import os, re

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
        self.file_name = dockerutils.getFileName()
        self.file_dir = dockerutils.getFileDir()
        components = self.file_dir.split(os.sep)
        self.project_dir = str.join(os.sep, components[:components.index("src")])
        self.file_dir_relative_to_project = str.join(os.sep, components[components.index("src"):])
        self.file_dir_relative_to_src = str.join(os.sep, components[components.index("src")+1:])
        
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
            opt_volume =  " -v \"" + self.project_dir+"/\":/leinproject"
            opt_temporary = " -t"
            opt_working_dir = " -w=\""+ "/leinproject/" + "\""
            image = " " + self.docker_image + ":" + self.docker_image_tag
            build_cmd =  " " + self.docker_image_exe
            docker_cmd = dockerutils.getCommand()
            command = [docker_cmd + " run" + opt_volume + opt_temporary + ' ' + dockerutils.opt_cleanup + opt_working_dir + image + build_cmd]
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

