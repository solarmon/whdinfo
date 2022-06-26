
#
# whdinfo.py
#
# https://github.com/solarmon/whdinfo
#

ver = "v0.1"

import os
import sys
import struct
import binascii

from pathlib import Path

import zipfile
from lhafile import LhaFile

import colorama
from colorama import Fore, Back, Style
colorama.init()
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

#
#
#

data_dir_but_no_ws_CurrentDir = []
whdload_installer = []

flags_dict = {
	1: 'WHDLF_Disk',
	2: 'WHDLF_NoError',
	4: 'WHDLF_EmulTrap',
	8: 'WHDLF_NoDivZero',
	16: 'WHDLF_Req68020',
	32: 'WHDLF_ReqAGA',
	64: 'WHDLF_NoKbd',
	128: 'WHDLF_EmulLineA',
	256: 'WHDLF_EmulTrapV',
	512: 'WHDLF_EmEmulChkul',
	1024: 'WHDLF_EmulPriv',
	2048: 'WHDLF_EmulLineF',
	4096: 'WHDLF_ClearMem',
	8192: 'WHDLF_Examine',
	16384: 'WHDLF_EmulDivZero',
	32768: 'WHDLF_EmulIllegal'
}

rawkeycodes = {
'00':'` ~',
'01':'1 !',
'02':'2 @',
'03':'3 #',
'04':'4 $',
'05':'5 %',
'06':'6 ^',
'07':'7 &',
'08':'8 *',
'09':'9 (',
'0A':'0 )',
'0B':'- _',
'0C':': +',
'0D':'|',
'0E':'',
'0F':'0',
'10':'Q',
'11':'W',
'12':'E',
'13':'R',
'14':'T',
'15':'Y',
'16':'U',
'17':'I',
'18':'O',
'19':'P',
'1A':'[ {',
'1B':'] }',
'1C':'',
'1D':'1',
'1E':'2',
'1F':'3',
'20':'A',
'21':'S',
'22':'D',
'23':'F',
'24':'G',
'25':'H',
'26':'J',
'27':'K',
'28':'L',
'29':'; :',
'2A':'\' "',
'2B':'',
'2C':'',
'2D':'4',
'2E':'5',
'2F':'6',
'30':'',
'31':'Z',
'32':'X',
'33':'C',
'34':'V',
'35':'B',
'36':'N',
'37':'M',
'38':', <',
'39':'. >',
'3A':'/ ?',
'3B':'',
'3C':'.',
'3D':'7',
'3E':'8',
'3F':'9',
'40':'Space bar',
'41':'Back Space',
'42':'Tab',
'43':'Enter',
'44':'Return',
'45':'Esc',
'46':'Del',
'47':'',
'48':'',
'49':'',
'4A':'-',
'4B':'',
'4C':'Up arrow',
'4D':'Down arrow',
'4E':'Forward arrow',
'4F':'Backward arrow',
'50':'F1',
'51':'F2',
'52':'F3',
'53':'F4',
'54':'F5',
'55':'F6',
'56':'F7',
'57':'F8',
'58':'F9',
'59':'F10',
'5A':'(',
'5B':')',
'5C':'/',
'5D':'*',
'5E':'+',
'5F':'HELP',
'60':'Left Shift',
'61':'Right Shift',
'62':'Caps Lock',
'63':'Ctrl',
'64':'Left Alt',
'65':'Right Alt',
'66':'Left Amiga',
'67':'Right Amiga'
}

#
#
#

def do_dir(filepath):

	lha_file_count = 0
	
	for dirName, subdirList, fileList in os.walk(filepath):
	
		#print()
		#print("dirName:",dirName)
		
		#print()
		#print("subdirList:",subdirList)
		
		#print()
		#print("fileList:",fileList)
		
		for fname in fileList:
		
			filename, file_extension = os.path.splitext(fname)
			
			if (file_extension.lower() == '.lha'):
				
				#if do_whdload_lha_file(str(Path(dirName) / fname)):
				if do_whdload_lha_file(str(Path(dirName) / fname)):
					lha_file_count += 1	# increment valid lha file count
					
	return lha_file_count

def do_whdload_lha_file(file):

	valid_lha_file = False

	filename, file_extension = os.path.splitext(file)
	basename, basename_extension = os.path.splitext(os.path.basename(file))
	
	try:
	
		lf = LhaFile(file, 'r')
			
	except:
	
		print()
		print("-----")
		print()
		#print("lf.lhaname():")
		print(Fore.YELLOW + "# LHA File: " + file + Style.RESET_ALL)
		print("+ Name:",basename)
		print()
		print(Fore.RED + "### Not valid LHA file! ###" + Style.RESET_ALL)
		
	else:
	
		valid_lha_file = True
		
		ws_CurrentDir_found = False
		ws_CurrentDir = ""
		
		data_dir_found = False
		data_dir = ""
		install_file_found = False
		slave_icon_found = False
		
		#print()
		#print(os.path.join(dirName, fname))
		
		print()
		print("-----")
		print()
		#print("lf.lhaname():")
		print(Fore.YELLOW + "# LHA File: " + lf.lhaname() + Style.RESET_ALL)
		print("+ Name:",basename)
		
		#print()
		#print("lf.namelist():")
		#print(lf.namelist())
		#print()
		
		#print()
		#print("infolist:")
		#print(lf.infolist())
		
		for lhafile_entry in lf.namelist():
		
			lfilename, lfile_extension = os.path.splitext(lhafile_entry)
			lbasename = os.path.basename(lhafile_entry)
			
			#path = Path(lhafile_entry)
			#parent_dir = path.parent.absolute()
			#print("Parent Dir:",parent_dir)
			
			parent_dir = os.path.dirname(lhafile_entry)
			#print("Parent Dir:",parent_dir)
			parent_basename = os.path.basename(parent_dir)
			#print("parent_basename:",parent_basename)
			
			#print("LHA item:", lhafile_entry, "| lbasename:", lbasename, "| lfile_extension: ", lfile_extension)
			
			if "disk." in lhafile_entry.lower():
				print(Fore.GREEN + "+ Disk File: " + lhafile_entry + Style.RESET_ALL)
			
			if not data_dir_found:
				#if "data" in parent_dir:
				if parent_basename == "data":
					data_dir_found = True
					data_dir = parent_basename
					print(Fore.GREEN + "+ Data Dir: " + parent_dir + Style.RESET_ALL)
					
			if((lfile_extension.lower() == '.slave')):
			
				slave_basename, slave_ext = os.path.splitext(lbasename)
				#print("slave_basename:",slave_basename)
				slave_icon = slave_basename + ".info"
				if slave_icon in lf.namelist():
					slave_icon_found = True
					print(Fore.CYAN + "+ Slave Icon: " + slave_icon + Style.RESET_ALL)
				else:
					print(Fore.RED + "+ Slave Icon: " + "NOT FOUND !!" + Style.RESET_ALL)
				
				print(Fore.CYAN + "+ Slave File: " + lhafile_entry + Style.RESET_ALL)
				
				slave_bytes = lf.read(lhafile_entry)
				#print("slave_bytes: ",slave_bytes
				
				ws_CurrentDir = do_slave_data(slave_bytes)
				
				if ws_CurrentDir:
					ws_CurrentDir_found = True
			
			if not install_file_found:			
				if "install" in lhafile_entry.lower():
					install_file_found = True
					print(Fore.RED + "+ Install File: " + lhafile_entry + Style.RESET_ALL)
		
		if not ws_CurrentDir_found and data_dir_found:
			print()
			print(Fore.RED + "!!! No ws_CurrentDir set but data dir exists !!!" + Style.RESET_ALL)
			data_dir_but_no_ws_CurrentDir.append(basename)
					
		if ws_CurrentDir_found and data_dir:
			if ws_CurrentDir == data_dir:
				print()
				print(Fore.GREEN + "!!! ws_CurrentDir is same as data dir found !!!" + Style.RESET_ALL)
			else:
				print()
				print(Fore.RED + "!!! ws_CurrentDir is NOT same as data dir found !!!" + Style.RESET_ALL)
				
		if install_file_found and not slave_icon_found:
			whdload_installer.append(basename)
		
		return valid_lha_file
		
def do_slave_file(file):
	with open(file, "rb") as f: # Slave has data path
		slave_bytes = f.read()
		do_slave_data(slave_bytes)
		
def do_slave_data(slave_bytes):

	ws_CurrentDir_found = False
	ws_CurrentDir = ""
	
	slave_bytes_length = sys.getsizeof(slave_bytes)	# Calculate the size of the data
	slave_hunk_header = slave_bytes[0:31]	# 32 bytes
	data = slave_bytes[32:slave_bytes_length]
	#print("slave_bytes_length: ",slave_bytes_length)
	#print("slave_hunk_header: ",slave_hunk_header)
	
	#print("data[0:20]: ",data[0:20])
	
	#
	#
	#
	
	#ws_Security = data[0:3]	# ws_Security (4)
	ws_Security = struct.unpack_from('>L', data[0:])[0]	# ws_Security (4 bytes)
	
	#print()
	print(Fore.YELLOW + "  - ws_Security: " + Style.RESET_ALL + str(ws_Security) + " (" + hex(ws_Security) + ")")
	
	#
	#
	#
	
	#ws_ID = data[4:12]	# ws_ID (8) - should be "WHDLOADS" for a slave file
	ws_ID = struct.unpack_from('8s', data[4:])[0].decode('iso-8859-1') # ws_ID (8 bytes) (8s = 8 byte string) - should be "WHDLOADS" for a slave file
	
	print(Fore.YELLOW + "  - ws_ID: " + Style.RESET_ALL + ws_ID)
	
	#if ws_ID=="WHDLOADS":	# If wd_ID contains "WHDLOADS" then it is a WHDLoad slave file
		#print("This is a slave file!")	#
	
	#
	# ws_Version
	#
	
	ws_Version = struct.unpack_from('>H', data[12:])[0]	# ws_Version (UWORD = H = unsigned short = integer (2))
	
	#print()
	print(Fore.YELLOW + "  - ws_Version: " + Style.RESET_ALL + str(ws_Version))
	
	#
	# ws_Flags
	#
	
	ws_Flags = struct.unpack_from('>H', data[14:])[0]	# ws_Version (UWORD = H = unsigned short = integer (2))
	
	# Parse flags
	flags = []
	for key, value in flags_dict.items():
		if ws_Flags & key:
			flags.append(value)
	
	print(Fore.YELLOW + "  - ws_Flags: " + Style.RESET_ALL + str(ws_Flags) + " " + str(flags))
	
	#
	# ws_BaseMemSize
	#
	
	ws_BaseMemSize = struct.unpack_from('>L', data[16:])[0]	# ws_BaseMemSize (ULONG = L = unsigned long = integer (4))
	
	#print()
	print(Fore.YELLOW + "  - ws_BaseMemSize: " + Style.RESET_ALL + str(ws_BaseMemSize))
	
	#
	# ws_ExecInstall
	#
	
	ws_ExecInstall = struct.unpack_from('>L', data[20:])[0]	# ws_ExecInstall (ULONG = L = unsigned long = integer (4)) - obsolete, must be set to 0
	
	#print()
	print(Fore.YELLOW + "  - ws_ExecInstall: " + Style.RESET_ALL + str(ws_ExecInstall))
	
	#
	# ws_GameLoader
	#
	
	ws_GameLoader_offset = struct.unpack_from('>H', data[24:])[0] # ws_GameLoader (RPTR) (2)
	ws_GameLoader = read_string(ws_GameLoader_offset, data)
	
	#print()
	print(Fore.YELLOW + "  - ws_GameLoader_offset: " + Style.RESET_ALL + str(ws_GameLoader_offset) + " (" + hex(ws_GameLoader_offset) + ")")
	print(Fore.YELLOW + "  - ws_GameLoader: " + Style.RESET_ALL + ws_GameLoader)
	#
	#
	#
	
	ws_CurrentDir_offset = struct.unpack_from('>H', data[26:])[0] # ws_CurrentDir (RPTR) (2)
	ws_CurrentDir = read_string(ws_CurrentDir_offset, data)
	
	if ws_CurrentDir:
		ws_CurrentDir_found = True
	
	#print("ws_CurrentDir_offset:",ws_CurrentDir_offset," (",hex(ws_CurrentDir_offset),")")
	print(Fore.YELLOW + "  - ws_CurrentDir: " + Style.RESET_ALL + ws_CurrentDir)
	
	#
	# ws_DontCache
	#
	
	ws_DontCache_offset = struct.unpack_from('>H', data[28:])[0] # ws_DontCache (RPTR) (2)
	#ws_DontCache_offset = data[28:29]
	
	print(Fore.YELLOW + "  - ws_DontCache_offset: " + Style.RESET_ALL + str(ws_DontCache_offset))
	ws_DontCache = read_string(ws_DontCache_offset, data)
	print(Fore.YELLOW + "  - ws_DontCache: " + Style.RESET_ALL + ws_DontCache)
	
	#
	# Version dependent
	#
	
	if (ws_Version >= 4):
		#print()
		#print("  * ws_Version >= 4")
		ws_keydebug = binascii.hexlify(struct.unpack_from('c', data[30:])[0]).decode('iso-8859-1')	# UBYTE = c = char (1)
		print(Fore.YELLOW + "  - ws_keydebug: " + Style.RESET_ALL + ws_keydebug)
		
		ws_keyexit = binascii.hexlify(struct.unpack_from('c', data[31:])[0]).decode('iso-8859-1')		# UBYTE c = char (1)
		print(Fore.YELLOW + "  - ws_keyexit: " + Style.RESET_ALL + ws_keyexit + " (" + rawkeycodes[ws_keyexit.upper()] + ")")
			
	if (ws_Version >= 8):
		#print()
		#print("  * ws_Version >= 8")
		ws_ExpMem = struct.unpack_from('>L', data[32:])[0]	# ULONG = L = unsigned long = integer (4)
		print(Fore.YELLOW + "  - ws_ExpMem: " + Style.RESET_ALL + str(ws_ExpMem))
		 
	if (ws_Version >= 10):
		#print()
		#print("  * ws_Version >= 10")
		ws_name_offset = struct.unpack_from('>H', data[36:])[0]	# UWORD = H = unsigned short = integer (2)
		ws_name = read_string(ws_name_offset, data)
		#print("  - ws_name_offset:",ws_name_offset)
		print(Fore.YELLOW + "  - ws_name: " + Style.RESET_ALL + ws_name)
		
		ws_copy_offset = struct.unpack_from('>H', data[38:])[0]	# UWORD = H = unsigned short = integer (2)
		ws_copy = read_string(ws_copy_offset, data)
		#print("  - ws_copy_offset:",ws_copy_offset)
		print(Fore.YELLOW + "  - ws_copy: " + Style.RESET_ALL + ws_copy)
		
		ws_info_offset = struct.unpack_from('>H', data[40:])[0]	# UWORD = H = unsigned short = integer (2)
		ws_info = read_string(ws_info_offset, data)
		#print("  - ws_info_offset:",ws_info_offset)
		print(Fore.YELLOW + "  - ws_info: " + Style.RESET_ALL + ws_info)
	
	if (ws_Version >= 16):
		#print()
		#print("  * ws_Version >= 16")
		ws_kickname_offset = struct.unpack_from('>H', data[42:])[0]	# UWORD = H = unsigned short = integer (2)
		ws_kickname = read_string(ws_kickname_offset, data)
		print(Fore.YELLOW + "  - ws_kickname: " + Style.RESET_ALL + ws_kickname)
		
		ws_kicksize = struct.unpack_from('>L', data[44:])[0]		# ULONG = L = unsigned long = integer (4)
		print(Fore.YELLOW + "  - ws_kicksize: " + Style.RESET_ALL + str(ws_kicksize))
		
		ws_kickcrc = struct.unpack_from('>H', data[48:])[0]		# UWORD = H = unsigned short = integer (2)
		print(Fore.YELLOW + "  - ws_kickcrc: " + Style.RESET_ALL + str(ws_kickcrc) + " (" + hex(ws_kickcrc) + ")")
		
	if (ws_Version >= 17):
		#print()
		#print("  * ws_Version >= 17")
		ws_config_offset = struct.unpack_from('>H', data[50:])[0]		# UWORD = H = unsigned short = integer (2)
		ws_config = read_string(ws_config_offset, data)
		
		print(Fore.YELLOW + "  - ws_config: " + Style.RESET_ALL + ws_config)
		#ws_config = read_string(ws_config_offset, data).split(';')
		#print("    - ws_config:",ws_config)

	version_string_offset = data.find(b"$VER:")	# Find start position of "$VER:"
	version_string = read_string(version_string_offset, data)
	
	if version_string:
		print()
		print(Fore.YELLOW + "  - Version String: " + Style.RESET_ALL + version_string)
	
	print()
	
	return ws_CurrentDir
				
def read_string(offset, data):

	if offset > 0:
		next_zero_offset = data.find(0,offset)	# Find next '00' byte
		string = data[offset:next_zero_offset].decode("ascii","ignore")
		return string
	else:
		return ""
#
#
#

#
#
#

print()
print("whdinfo.py",ver,"by solarmon")
print()

#print('cmd entry:', sys.argv)

lha_file_count = 0

if len(sys.argv) > 1:
	filepath = sys.argv[1]
else:

	print("Usage:")
	print()
	print("python whdinfo.py <path>")
	print()
	print("Where <path> can be a path to a:")
	print()
	print("* directory")
	print("* .lha file")
	print("* .slave file")
	print()
	print("If a directory path, then it will be recursively processed.")
	exit()

print("File Path:",filepath)

if os.path.exists(filepath) != True:
	print("File path not found!")
	exit()

if os.path.isdir(filepath):

	#print("Directory")
	
	lha_file_count = do_dir(filepath)

elif os.path.isfile(filepath):

	filename, file_extension = os.path.splitext(filepath.lower())

	if (file_extension == '.lha'):

		#print("LHA file")
		
		if do_whdload_lha_file(filepath):
			lha_file_count += 1	# increment valid lha file count

	elif (file_extension == '.slave'):

		#print("Slave file")
		
		print()
		print(Fore.CYAN + "+ Slave File: " + filepath + Style.RESET_ALL)
		do_slave_file(filepath)	
		
	else:
	
		print("Unsupported file")

if(lha_file_count):
	print()
	print ("#####")
	print()
	print("Number of WHDLoad LHA files processed: " + str(lha_file_count))

if(data_dir_but_no_ws_CurrentDir):
	print()
	print ("#####")
	print()
	print("WHDLoad LHA packages with a data directory but with no ws_CurrentDir set (" + str(len(data_dir_but_no_ws_CurrentDir)) + "):")
	print()
	for item in data_dir_but_no_ws_CurrentDir:
		print(Fore.RED + item + Style.RESET_ALL)

if(whdload_installer):
	print()
	print ("#####")
	print()
	print("WHDLoad LHA installer packages (" + str(len(whdload_installer)) + "):")
	print()
	for item in whdload_installer:
		print(Fore.RED + item + Style.RESET_ALL)
exit()