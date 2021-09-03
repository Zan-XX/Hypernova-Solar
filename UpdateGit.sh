git add .
git pull
read -p "Please enter a commit name or phrase: " name; \
git commit -m "$name"
git push -u https://github.com/maxsyrett/Hypernova-Solar.git main
