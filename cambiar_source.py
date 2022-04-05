import json
import sys
 
# Opening JSON file
nombre = sys.argv[1]
notebook = nombre + ".ipynb" 
new_source = nombre + ".py"
note_f = open(notebook,"r")
src_f = open(new_source,"r")
 
# returns JSON object as
# a dictionary
json_note = json.load(note_f)
json_note['cells'][0]['source'] = src_f.read()
# Closing file
note_f.close()

#escribir el cambio en la libreta 
with open(notebook, "w") as outfile:
    json.dump(json_note, outfile)
