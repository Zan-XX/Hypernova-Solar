git add .
git pull
set /p name=Please enter a commit name or phrase:
git commit -m "%name%"
git push -u origin main
