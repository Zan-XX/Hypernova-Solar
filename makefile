#https://www.tutorialspoint.com/how-to-install-tkinter-in-python
all:
	git add .
	git pull
	@read -p "Please enter a commit name or phrase: " name; \
	git commit -m "$name"
	git push -u https://github.com/maxsyrett/Hypernova-Solar.git master

getstarted:
	pip3 install tk
	pip3 install python-can
