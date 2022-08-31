from win32gui import *
import win32con, os, colorama
from mem_edit import Process
os.system('cls')
os.system("mode 49,17")
hwnd = GetForegroundWindow()
SetWindowLong(hwnd,win32con.GWL_STYLE,GetWindowLong(hwnd,win32con.GWL_STYLE) & ~(win32con.WS_SIZEBOX | win32con.WS_MAXIMIZEBOX))
import ctypes, time, sys, threading, psutil
from ctypes import windll, WinDLL
windll.kernel32.SetConsoleTitleW("\u200b")
colorama.init()

class _CursorInfo(ctypes.Structure):
	_fields_ = [("size", ctypes.c_int),
				("visible", ctypes.c_byte)]
print("              Made by Nandi#0001\n")
ci = _CursorInfo()
handle = ctypes.windll.kernel32.GetStdHandle(-11)
ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
ci.visible = False
ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))

class changer:
	status = ""
	def __init__(self):
		threading.Thread(target=self.loading_title,).start()
		self.find_addr()

	def loading_title(self):
		i=0
		animation = '|/-\\'
		while 1:
			while self.status == "searching":
				time.sleep(0.1)
				windll.kernel32.SetConsoleTitleW(f"Searching  {animation[i % len(animation)]}")
				i+=1
			if self.status == "end":
				self.status = "set"
				windll.kernel32.SetConsoleTitleW("\u200b")
			time.sleep(0.1)

	def find_addr(self):
		while 1:
			pid = Process.get_pid_by_name('SoTGame.exe')
			if pid == None:
				self.status = "end"
				print("[\u001b[33m-\u001b[0m] Waiting for process...", end="\r")
			else:
				break
			time.sleep(2)
		input("[\u001b[34m~\u001b[0m] Set your FOV to 90 then press enter")
		with Process.open_process(pid) as p:
			self.status = "searching"
			freezeprocess = psutil.Process(pid)
			freezeprocess.suspend()
			addrs = p.search_all_memory(ctypes.c_float(90))
			freezeprocess.resume()
			self.status = "end"
			if len(addrs) != 0:
				print("[\u001b[32m+\u001b[0m] First search successful!\n")
			else:
				input("[\u001b[31m!\u001b[0m] First search failed!")
				os._exit(0)
			input("[\u001b[34m~\u001b[0m] Set your FOV to 60 then press enter")
			self.status = "searching"
			freezeprocess.suspend()
			addrs = p.search_addresses(addrs, ctypes.c_float(60))
			self.status = "end"
			freezeprocess.resume()
			if len(addrs) != 0:
				print("[\u001b[32m+\u001b[0m] Second search successful!\n")
			else:
				input("[\u001b[31m!\u001b[0m] Second search failed!")
				os._exit(0)
			input("[\u001b[34m~\u001b[0m] Set your FOV to 90 then press enter")
			self.status = "searching"
			freezeprocess.suspend()
			addrs = p.search_addresses(addrs, ctypes.c_float(90))
			self.status = "end"
			freezeprocess.resume()
			if len(addrs) == 1:
				print("[\u001b[32m+\u001b[0m] Third search successful, address found!\n")
			else:
				input("[\u001b[31m!\u001b[0m] Third search failed!")
				os._exit(0)
			ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
			ci.visible = True
			ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
			p.write_memory(addrs[0], ctypes.c_float(int(input("[\u001b[34m~\u001b[0m] FOV: "))))
			ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
			ci.visible = False
			ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
			input("[\u001b[32m+\u001b[0m] FOV changed!")
			os._exit(0)

if __name__ == '__main__':
	changer()