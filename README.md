cubeworld-dialogue-patcher
==========================

This patcher allows you to add and remove dialogue choices for NPCs.
This has been developed for the latest version of cubeworld as of 8/7/13, the changelog should show:
```
Patchnotes:
- Added an option to invert the y-axis
- Fixed a bug where MP could be regenerated with the 'O' key
- Fixed a bug where players could sell non-existing items from their inventory
- Improved some launcher issues
 ```


Requirements:
----------------
Python2.7 (or similiar)
	
Howto:
-----------------
Put dialogue_patcher.py in your 'Cube World' directory and run it with python (double clicking should work)
	
It should create a new folder 'dialogue' with 'stock.xml' inside, this is the default dialogue, to add more simply add more .xml files in the dialogue folder. The format of stock.xml should show how easy it is to create new dialogue. Note that files beginning with '_' will not be loaded.
	
Once you have the xml files you want in dialogue, run dialogue_patcher.py. It should tell you to replace Cube.exe with Cube_patched.exe. Just delete Cube.exe and rename Cube_patched.exe, a backup has already been created as Cube.exe.bak

Rollback:
-------------------
If you don't want the changes made, or it breaks something just delete Cube.exe and data4.db and rename Cube.exe.bak to Cube.exe then data4.db.bak to data4.db
