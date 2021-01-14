# Welcome!

## Port of Dash Apps
- Yang's Dash is Port 8082
- Eric's Dash is Port 8083
- Yuyou's Dash is Port 8084

## If you have time, please make your .ipynb a .py, and edit the top and end of the code.

### e.g.
### top of code
```
#app = JupyterDash(__name__) # comment it
app = dash.Dash(__name__) # new Line
application = app.server # new Line
```
### end of code
```
if __name__ == '__main__':
    #app.run_server(debug=True) # comment it
    application.run(host = '0.0.0.0', debug = True, port = 805X) # write your port number
```

## Basic Commands
### Download and Upload
- git init
- git clone git@github.com:wox080xow/Amazon-EC2.git
- git add fileName
- git commit -m 'Your Message'
- git checkout -b newBranchName
- git remote add newUpstreamName git@github.com:wox080xow/Amazon-EC2.git
- git push [-u upstreamName branchName]
- git fetch
  - to update and check the list of repository, just like "apt update" and then "apt list --upgradable"
- git merge upstreamName/branchName
  - to download the updated files from the chosen branch
### Check Status
- git status
- git log
- git branch
- git remote -v
- git diff

## Advanced Commands
- git reset -- fileName
  - to unstage files..

- git rm fileName
  - to untrack and "delete" file

- git rm -r <directory> --cached
  - to untrack directory and make GitHub tidy
