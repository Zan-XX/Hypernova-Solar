all:
	git add .
	git pull
	@read -p "Please enter a commit name or phrase: " name; \
	git commit -m "$name"
	git push -u origin main


getstarted:
	pip3 install tkinter
	pip3 install python-can
