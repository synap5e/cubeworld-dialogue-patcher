'''

Dialogue patcher by synap5e

Version 0.1


'''

import sys, sqlite3, os, struct, re
import xml.etree.ElementTree as ET

# This value is used as mod to limit the random number used for selecting dialogue
# to within the number of dialogue strings
dialogue_count_offset = 0xE450C

# This array is used to encode and decode the resource files 
data_key = [
0x00001092, 0x0000254F, 0x00000348, 0x00014B40, 0x0000241A, 0x00002676,
0x0000007F, 0x00000009, 0x0000250B, 0x0000018A, 0x0000007B, 0x000012E2,
0x00007EBC, 0x00005F23, 0x00000981, 0x00000011, 0x000085BA, 0x0000A566,
0x00001093, 0x0000000E, 0x0002D266, 0x000007C3, 0x00000C16, 0x0000076D,
0x00015D41, 0x000012CD, 0x00000025, 0x0000008F, 0x00000DA2, 0x00004C1B,
0x0000053F, 0x000001B0, 0x00014AFC, 0x000023E0, 0x0000258C, 0x000004D1,
0x00000D6A, 0x0000072F, 0x00000BA8, 0x000007C9, 0x00000BA8, 0x0000131F,
0x000C75C7, 0x0000000D
]

if not os.path.isdir('./dialogue'):
	os.mkdir('./dialogue')

def swap(data, index1, index2):
	temp = data[index1]
	data[index1] = data[index2]
	data[index2] = temp

def encoder(data, decode):
	data = bytearray(data)
	size = len(data)
	r = range(size)
	if decode:
		r = reversed(r)
	for i in r:
		location = data_key[i % 44] + i
		swap(data, i, location % size)
	for i in range(size):
		data[i] = 0xFF - data[i]
	return data

def load_external_dialogue(path):
	root = ET.parse(path)
	dialogue = list()
	for random in root.findall('speech'):
		dialogue.append(random.text)
	return dialogue

print "Backing up files"
f = file('Cube.exe', 'rb')
data = bytearray(f.read())
f.close()
f = file('Cube.exe.bak', 'wb')
f.write(data)
f.close()
f = file('data4.db', 'rb')
d = f.read()
f.close()
f = file('data4.db.bak', 'wb')
f.write(d)
	
print "Reading Cube.exe"
exe_dialogue_count = struct.unpack('<i', str(data[dialogue_count_offset:dialogue_count_offset+4]))[0]
print "Found dialogue limit: %d" % exe_dialogue_count
print ""

conn = sqlite3.connect('data4.db')
dict_en = encoder(conn.execute("SELECT value FROM blobs WHERE key=?", [u'dict_en.xml']).fetchone()[0], True)

if (not os.path.isfile('./dialogue/stock.xml')) and (not os.path.isfile('./dialogue/_stock.xml')):
	print "stock dialogue not found, extracting"
	print "Reading data4.db"
	print "Parsing dict_en.xml"
	stock = file('./dialogue/stock.xml', 'wc')
	stock.write('<?xml version="1.0" encoding="utf-8"?>\r\n\r\n<root>\r\n\r\n')
	root = ET.fromstring(str(dict_en))
	count = 0
	for random in root.findall('speech'):
		if re.match('random:[0-9]+', random.get('key')):
			count+=1
			stock.write("  <speech>" + random.text + "</speech>\r\n\r\n")
	stock.write('</root>')
	stock.close()
	print "written %d strings of stock dialogue to ./dialogue/stock.txt" % count
	print ""

print "Loading dialogue from ./dialogue/"
dialogue = list()
for f in os.listdir('./dialogue/'):
	f = './dialogue/' + str(f)
	if os.path.isfile(f) and not str(os.path.basename(f)).startswith("_"):
		dialogue += load_external_dialogue(f)
print "Loaded %d strings" % len(dialogue)
print ""

print "Removing strings from dict_en.xml"
root = ET.fromstring(str(dict_en))
for random in root.findall('speech'):
	if re.match('random:[0-9]+', random.get('key')):
		root.remove(random)
print "Adding %d strings to dict_en.xml from ./dialogue/" % len(dialogue)
dict_en = str(dict_en)[:-8]
for index in range(1, len(dialogue)+1):
	dict_en += '  <speech key="random:%d">%s</speech>\r\n\r\n' % (index, dialogue[index-1])
dict_en += '</root>'
print ""

print "Writing dict_en.xml to data4.db"
conn.execute("UPDATE blobs SET value=? WHERE key=?", (sqlite3.Binary(encoder(dict_en, False)), u'dict_en.xml'))
conn.commit()
conn.close()
print ""

print "Patching Cube.exe to support %d strings" % len(dialogue)
data[dialogue_count_offset:dialogue_count_offset+4] = struct.pack('<i', len(dialogue))
f = file('Cube_patched.exe', 'wb')
f.write(data)
f.close()
print "Written patched file to Cube_patched.exe"
print ""

print "DONE!"
print "-"*60
print "please replace Cube.exe with Cube_patched.exe"
print ""
print "press enter to close"
raw_input()
