# Use RAW mode to read the complete contents without hidden texts...

## Port of Dash Apps
- Yang's Dash use Port 8082
- Eric's Dash use Port 8083
- Yoyou's Dash use Port 8084

##If you have time, please make your .ipynb a .py, and edit the top and end of the code.

### e.g.
### top of code
#app = JupyterDash(__name__) # comment it
```
app = dash.Dash(__name__) # new Line
application = app.server # new Line
```
### end of code
```
if __name__ == '__main__':
    #app.run_server(debug=True) # comment it
    application.run(host = '0.0.0.0', debug = True, port = 805X) # write your port number
```

## Commands
- git init
- git clone http...
- git add <file>
- git commit -m 'Your Message'
- git remote -v
- git branch

## Advanced Commands
- git reset -- <file>
  - to unstage deleted files..

- git rm -r <directory> --cached
  - to untracked deleted files and make GitHub tidy
