1) Check out the repository

2) Create and enter your virtual environment
virtualenv <repository/path>/ENV
source <repository/path>/ENV/bin/activate

3) Install the requirements
pip install -r requirements.txt

4) Edit upload.py to set the proper upload path
vi <repository/path>/upload.py
Edit the line with UPLOAD_PATH =

5) Run the flask-based server
python upload.py

6) Point browser to <machine ip>:5000 (default port)

NOTE: The javascript is not fully functional (it has some element bugs in it).
Only choose one file at a time to upload, and reload the page before sending 
another. Files will be chunked and placed in your UPLOAD_PATH directory.
Files do not currently retain their filenames, but this can be corrected in a
later version of the code

