#!/usr/bin/env python3

# created by n0w4n
# automate your list of programs to be installed on a new system
# build for debian based operating systems (use of apt)

import sys, subprocess


# list for programs and newly programs to install
apt_programs = ["wireshark", "pip3", "docker.io", "terminator"] # add programs to be installed via apt here
pip_programs = ["docker-compose"] # add programs to be installed via pip here
install_apt = []
install_pip = []
 

def installation_check(program, module):
	if module == "apt":
		try:
			cmd = f"dpkg -s {program}"
			subprocess.check_output(["dpkg", "-s", program, "|", "grep 'Status: install ok installed'"], stderr=subprocess.DEVNULL)
			return True
		except subprocess.CalledProcessError:
			return False
	if module == "pip":
		try:
			subprocess.check_output(["pip3", "show", program], stderr=subprocess.DEVNULL)
			return True
		except subprocess.CalledProcessError:
			return False


def program_installation(program, module):
	if module == "apt":
		try:
			subprocess.run(['sudo', 'apt', '-y', 'install', program], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
			return True
		except subprocess.CalledProcessError as e:
			error_message = None
			if e.stderr:
				error_lines = e.stderr.decode().splitlines()
				error_message = next((line for line in error_lines if "E:" in line), None)
			return error_message
	if module == "pip":
		try:
			subprocess.run(['pip', 'install', program], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
			return True
		except subprocess.CalledProcessError as e:
			error_message = None
			if e.stderr:
				error_lines = e.stderr.decode().splitlines()
				error_message = next((line for line in error_lines if "No matching distribution found" in line), None)
			return error_message 


def main():
	print(f"[-] checking programs:")
	# checking for installed apt programs
	for program in apt_programs:
		result = installation_check(program, "apt")
		if result is not None:
			print(f"    {program} is installed")
		else:
			print(f"    {program} is not installed")
			install_apt.append(program)
	# checking for installed pip programs
	for program in pip_programs:
		result = installation_check(program, "pip")
		if result is True:
			print(f"    {program} is installed")
		else:
			print(f"    {program} is not installed")
			install_pip.append(program)
	# if needed, installing missing programs
	if len(install_apt) != 0 or len(install_pip) != 0: 
		text = f"[-] Installing missing programs (Y/n)?: "
		user_input = input(text)
		if user_input.lower() == "y" or user_input.lower() == "yes":
			print(f"[-] Installing programs:")
			for program in install_apt:
				result = program_installation(program, "apt")
				if result is True:
					print(f"    {program} installed")
				else:
					print(f"    {result}")
			for program in install_pip:
				result = program_installation(program, "pip")
				if result is True:
					print(f"    {program} installed")
				else:
					print(f"    {result}")


if __name__ == "__main__":
	main()
