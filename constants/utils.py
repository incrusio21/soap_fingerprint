import json
import os
import sys

from constants import fernet_key

def find_data_file(datadir, filename: str, encrypt=False):
    decrypted = False
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
        if encrypt:
            decrypted = True
            filename, _ = os.path.splitext(filename)
        
    with open(os.path.join(datadir, filename)) as stream:
        file = stream.read()
        if decrypted:
            # decrypting the file
            file = fernet_key.decrypt(file)
    
    return file 

def set_args(args, items):
    for row in items:
        args.setdefault(row, items[row])

def as_json(obj, indent=1, separators=None) -> str:
	if separators is None:
		separators = (",", ": ")

	try:
		return json.dumps(
			obj, indent=indent, sort_keys=True, separators=separators
		)
	except TypeError:
		return json.dumps(obj, indent=indent, separators=separators)
