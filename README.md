cubeworld-dialogue-patcher
==========================

This patcher allows you to add and remove dialogue choices for NPCs

Requirements:
	Python2.7 (or similiar)
	
Howto:
	Put dialogue_patcher.py in your 'Cube World' directory and run it with python (double clicking should work)
	
	It should create a new folder 'dialogue' with 'stock.xml' inside, this is the default dialogue, to add more
	simply add more .xml files in the dialogue folder. The format of stock.xml should show how easy it is to
	create new dialogue. Note that files beginning with '_' will not be loaded.
	
	Once you have the xml files you want in dialogue, run dialogue_patcher.py. It should tell you to replace Cube.exe
	with Cube_patched.exe. Just delete Cube.exe and rename Cube_patched.exe, a backup has already been created as 
	Cube.exe.bak