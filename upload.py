from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from werkzeug import secure_filename
import os
import re

UPLOAD_PATH = "/tmp"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        saved_filenames = []
        remote_name = request.form['name']
        chunk_count = int(request.form['chunks'])
        chunk_index = int(request.form['chunk'])
        for key, upload_file in request.files.iteritems():
            if upload_file:
                filename = secure_filename("%s_%s" % (upload_file.filename, remote_name))
                parts_dir = os.path.join(UPLOAD_PATH, "%s_parts" % filename)
                if not os.path.exists(parts_dir):
                    os.mkdir(parts_dir)
                destination_path = os.path.join(parts_dir, "%s_%s" % (filename, chunk_index))
                upload_file.save(destination_path)
                print "Saving file to %s" % destination_path
                saved_filenames.append(filename)
                if chunk_index == chunk_count - 1:
                    print "Joining parts"
                    join_parts(parts_dir)
        return saved_filenames[0]
    else:
        return render_template('basic.html', name=__name__)


def join_parts(parts_directory):
    base_dir, parts_name = os.path.split(parts_directory)
    parts_pattern = r"(.+)_parts"
    parts_result = re.match(parts_pattern, parts_name)
    if not parts_result:
        raise Exception("Invalid name for parts directory")
    target_name = parts_result.group(1)
    target_path = os.path.join(base_dir, target_name)
    with open(target_path, 'wb+') as target:
        parts_list = os.listdir(parts_directory)
        parts_list.sort(lambda x,y: cmp( int(x.split('_')[-1]), int(y.split('_')[-1])))
        for part in parts_list:
            part_path = os.path.join(parts_directory, part)
            with open(part_path, "rb+") as part_handle:
                buf = part_handle.read(1024 * 1024 * 10)
                while buf:
                    target.write(buf)
                    buf = part_handle.read(1024 * 1024 * 10)

    
if __name__ == '__main__':
    app.debug = True
    app.run()


