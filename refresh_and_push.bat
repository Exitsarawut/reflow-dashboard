@echo off

curl http://127.0.0.1:5000/refresh

git add .
git commit -m "update data"
git pull origin main --rebase
git push

pause