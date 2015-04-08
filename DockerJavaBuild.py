from . import dockerutils
import sublime, sublime_plugin
import os


class DockerJavaBuildCommand(sublime_plugin.WindowCommand):

    type = "RUN"
    docker_image = "java"
    docker_image_tag = "2.7xx" # Value seems to be unused?
    build_exe = "javac"
    run_exe = "/src/javarun.sh"

    def run(self, type="RUN", docker_image="java", docker_image_tag="2.7"):
        self.type = type
        self.docker_image = docker_image
        self.docker_image_tag = docker_image_tag
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
            #build_cmd =  " " + self.build_exe + " \"/src/"+self.file_name + "\" && " + self.run_exe + " " + os.path.splitext(self.file_name)[0]
            build_cmd =  " " + self.run_exe + " \"/src/" + self.file_name + "\""
            docker_cmd = dockerutils.getCommand()
            command = [docker_cmd + " run" + opt_volume + opt_temporary + ' ' + dockerutils.opt_cleanup + image + build_cmd]
        elif self.type == "BUILD":
            opt_volume =  " -v " + self.file_dir+"/:/src"
            opt_temporary = " -t"
            image = " " + self.docker_image + ":" + self.docker_image_tag
            build_cmd =  " " + self.build_exe + " /src/"+self.file_name
            docker_cmd = dockerutils.getCommand()
            command = [docker_cmd + " run" + opt_volume + opt_temporary + ' ' + dockerutils.opt_cleanup + image + build_cmd]
            dockerutils.logDockerCommand(command)
        else:
            self.errorMessage("Unknown command: " + self.type)
            return


        dockerutils.getView().window().run_command("exec", { 'kill': True })
        dockerutils.getView().window().run_command("exec", {
            'shell': True,
            'cmd': command,
            'working_dir' : self.file_dir
        })

    
