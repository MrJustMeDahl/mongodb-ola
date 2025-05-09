from bson import decode_all
from bson.json_util import dumps

with open('./tweets.bson','rb') as f:
    data = decode_all(f.read())

with open("./tweets.json", "w") as outfile:
    outfile.write(dumps(data, indent=2))