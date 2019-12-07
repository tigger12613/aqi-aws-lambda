import json

def get_user_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        return data
    return False

def rewrite_user_data(filename,data):  
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        return True
    return False