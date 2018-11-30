import json
import os
import errno

def log(content):
    print('========>> %s ' % content)

def load_json(code):
    path = get_file_path(code, 'json')
    create_path(path)
    with open(path, 'r') as f:
        saved_data = json.load(f)
        log('从 %s 取出 %s' % (path, str(saved_data)))
        return saved_data


def save_json(code, key, value):
    path = get_file_path(code, 'json')
    create_path(path)
    saved_data={}
    if os.path.isfile(path):
        saved_data = load_json(code)
    saved_data[key] = value
    with open(path, 'w') as f:
        log('保存{%s:%s} 到 %s' % (key, value, path))
        json.dump(saved_data, f)


def get_img_path(code, filename):
    path = os.path.join('private/' + code, filename + r".png")
    return path


def get_file_path(code, filename):
    path = os.path.join('private/' + code, filename + r".txt")
    return path


def create_path(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise


if __name__ =='__main__':
    save_json('622300','你好','发看是发深V回家拿')
    save_json('622300','fsvdfv','vdfvfdsvf')