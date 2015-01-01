import User.dockerutils
import sublime, sublime_plugin
import os


class DockerJavaBuildCommand(sublime_plugin.WindowCommand):

    type = "RUN"
    docker_image = "java"
    docker_image_tag = "2.7xx" # Value seems to be unused?
    build_exe = "javac"
    run_exe = "java"

    def run(self, type="RUN", docker_image="java", docker_image_tag="2.7"):
        self.type = type
        self.docker_image = docker_image
        self.docker_image_tag = docker_image_tag
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
            build_cmd =  " " + self.build_exe + " /src/"+self.file_name + " && " + self.run_exe + " " + os.path.splitext(self.file_name)[0]
            command = ["docker run" + opt_volume + opt_temporary + opt_cleanup + image + build_cmd]
        elif self.type == "BUILD":
            opt_volume =  " -v " + self.file_dir+"/:/src"
            opt_temporary = " -t"
            opt_cleanup = " --rm"
            image = " " + self.docker_image + ":" + self.docker_image_tag
            build_cmd =  " " + self.build_exe + " /src/"+self.file_name
            command = ["docker run" + opt_volume + opt_temporary + opt_cleanup + image + build_cmd]
        else:
            self.errorMessage("Unknown command: " + self.type)
            return

        User.dockerutils.getView().window().run_command("exec", { 'kill': True })
        User.dockerutils.getView().window().run_command("exec", {
            'shell': True,
            'cmd': command,
            'working_dir' : self.file_dir
        })

    
