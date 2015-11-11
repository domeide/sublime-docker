import sublime, sublime_plugin
import time

hello_dir="/Users/mariolet/GitHub/sublime-docker/language-helloworlds/"
hello_java="HelloWorld.java"
hello_cpp="HelloWorld.cpp"
hello_perl="perl-version.pl"
hello_perl6="perl6-only.pl"
hello_python="python-version.py"
hello_ruby="rubyversion.rb"
hello_go="go-version.go"

args_default_python={"type": "RUN", "docker_image": "python", "docker_image_tag": "latest", "docker_image_exe": "python"}
args_default_ruby={"type": "RUN", "docker_image": "ruby", "docker_image_tag": "latest", "docker_image_exe": "ruby"}
args_default_go={"type": "RUN", "docker_image": "golang", "docker_image_tag": "latest", "docker_image_exe": "go run"}
args_default_perl={"type": "RUN", "docker_image": "perl", "docker_image_tag": "latest", "docker_image_exe": "perl"}
args_default_cpp={"type": "RUN", "docker_image": "gcc", "docker_image_tag": "latest", "docker_image_exe": "g++"}
args_default_java={"type": "RUN", "docker_image": "java", "docker_image_tag": "latest"}


class SublimeDockerTestsCommand(sublime_plugin.WindowCommand):

    def run(self):
    	self.test_python()
    	time.sleep(1)
    	self.test_ruby()
    	time.sleep(1)
    	self.test_golang()
    	time.sleep(1)
    	self.test_java()
    	time.sleep(1)
    	self.test_cpp()
    	time.sleep(1)
    	self.test_perl()

    def test_python(self):
    	self.window.open_file(hello_dir+hello_python)
    	self.window.run_command("docker_build",args_default_python)

    def test_ruby(self):
    	self.window.open_file(hello_dir+hello_ruby)
    	self.window.run_command("docker_build",args_default_ruby)

    def test_golang(self):
    	self.window.open_file(hello_dir+hello_go)
    	self.window.run_command("docker_build",args_default_go)

    def test_java(self):
    	self.window.open_file(hello_dir+hello_java)
    	self.window.run_command("docker_build",args_default_java)

    def test_cpp(self):
    	self.window.open_file(hello_dir+hello_cpp)
    	self.window.run_command("docker_build",args_default_cpp)

    def test_perl(self):
    	self.window.open_file(hello_dir+hello_perl)
    	self.window.run_command("docker_build",args_default_perl)

