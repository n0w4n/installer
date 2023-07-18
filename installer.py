#!/usr/bin/env python3

# created by n0w4n
# automate your list of programs to be installed on a new system

import sys, subprocess, shutil
from colorama import Fore, Style


# vars for coloring text
red = Fore.RED
green = Fore.GREEN
blue = Fore.BLUE
yellow = Fore.YELLOW
clear = Style.RESET_ALL

# list for programs and newly programs to install
apt_programs = ["wireshark", "pip3", "docker", "terminator"] # add programs to be installed via apt here
pip_programs = ["docker-compose"] # add programs to be installed via pip here
install_apt = []
install_pip = []
 

def installation_check(program, module):
	if module == "apt":
		check_program = shutil.which(program)
		return check_program
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
				error_message = next((line for line in error_lines if "Unable to locate package" in line), None)
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
	print(f"{blue}[-] checking programs:{clear}")
	# checking for installed apt programs
	for program in apt_programs:
		result = installation_check(program, "apt")
		if result is not None:
			print(f"    {green}{program} is installed{clear}")
		else:
			print(f"    {yellow}{program} is not installed{clear}")
			install_apt.append(program)
	# checking for installed pip programs
	for program in pip_programs:
		result = installation_check(program, "pip")
		if result is True:
			print(f"    {green}{program} is installed{clear}")
		else:
			print(f"    {yellow}{program} is not installed{clear}")
			install_pip.append(program)
	# if needed, installing missing programs
	if len(install_apt) != 0 or len(install_pip) != 0: 
		text = f"{blue}[-] Installing missing programs (Y/n)?:{clear} "
		user_input = input(text)
		if user_input.lower() == "y" or user_input.lower() == "yes":
			print(f"{blue}[-] Installing programs:{clear}")
			for program in install_apt:
				result = program_installation(program, "apt")
				if result is True:
					print(f"    {green}{program} installed{clear}")
				else:
					print(f"{red}    {result}{clear}")
			for program in install_pip:
				result = program_installation(program, "pip")
				if result is True:
					print(f"    {green}{program} installed{clear}")
				else:
					print(f"{red}    {result}{clear}")


if __name__ == "__main__":
	main()
