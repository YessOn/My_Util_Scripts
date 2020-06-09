def sort_by_ext(files):
	dots_sorted = sorted([i for i in files if ((i.startswith('.') and len(i.split(".")) <= 2) or i.endswith('.'))])
	for j in sorted([i.split(".")[::-1] for i in [i for i in files if not ((i.startswith('.') and len(i.split(".")) <= 2) or i.endswith('.'))]]):
		ext_sorted = ['.'.join(j[::-1]) for j in sorted([i.split(".")[::-1] for i in [i for i in files if not ((i.startswith('.') and len(i.split(".")) <= 2) or i.endswith('.'))]])]
	return dots_sorted + ext_sorted
if sort_by_ext(['1.cad', '1.bat', '1.aa']) == ['1.aa', '1.bat', '1.cad']:
	print(True)
else:
	print(False)
if sort_by_ext(['1.cad', '1.bat', '1.aa', '2.bat']) == ['1.aa', '1.bat', '2.bat', '1.cad']:
	print(True)
else:
	print(False)
if sort_by_ext(['1.cad', '1.bat', '1.aa', '.bat']) == ['.bat', '1.aa', '1.bat', '1.cad']:
	print(True)
else:
	print(False)
if sort_by_ext(['1.cad', '1.bat', '.aa', '.bat']) == ['.aa', '.bat', '1.bat', '1.cad']:
	print(True)
else:
	print(False)
if sort_by_ext(['1.cad', '1.', '1.aa']) == ['1.', '1.aa', '1.cad']:
	print(True)
else:
	print(False)
if sort_by_ext(['1.cad', '1.bat', '1.aa', '1.aa.doc']) == ['1.aa', '1.bat', '1.cad', '1.aa.doc']:
	print(True)
else:
	print(False)
if sort_by_ext(['1.cad', '1.bat', '1.aa', '.aa.doc']) == ['1.aa', '1.bat', '1.cad', '.aa.doc']:
	print(True)
else:
	print(False)
if sort_by_ext([".config","my.doc","1.exe","345.bin","green.bat","format.c","no.name.","best.test.exe"]) == [".config","no.name.","green.bat","345.bin","format.c","my.doc","1.exe","best.test.exe"]:
	print(True)
else:
	print(False)

print(sort_by_ext(['1.cad', '1.bat', '1.aa']), ['1.aa', '1.bat', '1.cad'])
print(sort_by_ext(['1.cad', '1.bat', '1.aa', '2.bat']), ['1.aa', '1.bat', '2.bat', '1.cad'])
print(sort_by_ext(['1.cad', '1.bat', '1.aa', '.bat']), ['.bat', '1.aa', '1.bat', '1.cad'])
print(sort_by_ext(['1.cad', '1.bat', '.aa', '.bat']), ['.aa', '.bat', '1.bat', '1.cad'])
print(sort_by_ext(['1.cad', '1.', '1.aa']), ['1.', '1.aa', '1.cad'])
print(sort_by_ext(['1.cad', '1.bat', '1.aa', '1.aa.doc']), ['1.aa', '1.bat', '1.cad', '1.aa.doc'])
print(sort_by_ext(['1.cad', '1.bat', '1.aa', '.aa.doc']), ['1.aa', '1.bat', '1.cad', '.aa.doc'])
print(sort_by_ext([".config","my.doc","1.exe","345.bin","green.bat","format.c","no.name.","best.test.exe"]), [".config","no.name.","green.bat","345.bin","format.c","my.doc","1.exe","best.test.exe"])