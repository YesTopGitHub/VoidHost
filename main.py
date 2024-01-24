from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)


@app.route('/')
def index():
  return '''<HTML>
  <HEAD>
  <TITLE>HomePage</TITLE>
  </HEAD>
  <BODY>
  <A HREF="/files">Files</A>
  <A HREF="/upload">Upload</A>
  </BODY>
  </HTML>'''


@app.route('/files', methods=['GET', 'POST'])
def files():
  if request.method == 'GET':
    file_links = []
    for file in os.listdir('uploads'):
      file_links.append(f'<a href="/download?file={file}">{file}</a>')
    return '<br>'.join(file_links)
  elif request.method == 'POST':
    filename = request.form['filename']
    entered_password = request.form['password']
    with open(f'passwords/{filename}.txt', 'r') as f:
      password = f.read()
    if entered_password == password:
      return send_from_directory('uploads', filename)
    else:
      return 'Incorrect password'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'GET':
    return '''
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="text" name="password" placeholder="Enter password">
                <input type="submit" value="Upload">
            </form>
        '''
  else:
    file = request.files['file']
    password = request.form['password']
    file.save(os.path.join('uploads', file.filename))
    with open(f'passwords/{file.filename}.txt', 'w') as f:
      f.write(password)
    return 'File uploaded successfully'


@app.route('/download', methods=['GET'])
def download():
  filename = request.args.get('file')
  return f'''
        <form action="/files" method="post">
            <input type="hidden" name="filename" value="{filename}">
            <input type="text" name="password" placeholder="Enter password">
            <input type="submit" value="Download">
        </form>
    '''


if __name__ == "__main__":
  app.run('0.0.0.0', 8080)
