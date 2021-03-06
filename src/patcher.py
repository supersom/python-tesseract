import os,collections,sys,platform
def isPython3():
	if sys.version_info > (3,0):
		return True
	else:
		return False
PYTHON3=isPython3()
		
class patcher:
	def __init__(self,incName,incFile,keywords):

		self.fName=incFile
		#self.fMinName="%s_mini.h"%incFile[:-2]
		self.fMinName=incFile
		self.incName=incName
		self.keywords=keywords
		self.lines=self.getLines(self.fName,incName)
		#self.patching()
	def getLines(self, fName,incName):
		mPaths=["/usr","/usr/local","/opt","/opt/local"]
		fullNames=[os.path.join(mPath,"include",incName,fName) for mPath in mPaths]
		#print fullNames
		for fullName in fullNames:
			if not os.path.exists(fullName):
				continue
			lines=open(fullName).read().split(";")
			return lines

	def lineParser(self,line,keywords):
		if "include" in line:
			KEYWORD_FOUND=None
			return line
		for s in keywords:
			if s not in line:
				continue
			head=[]
			slines=line.split("\n")
			for j,sline in enumerate(slines):
				if s not in sline:
					head.append(sline)
				else:
					headStr="\n".join(head)
					tailStr="\n"+"\n".join(slines[j:])
					KEYWORD_FOUND=s
					return s, headStr, tailStr
		return line

	def patching(self):
		fMinName,lines,keywords=self.fMinName,self.lines,self.keywords
		if not lines:
			print(("%s not existed"%self.fName))
			print(("Have you installed %s?"%self.incName))
			return False
		if self.keywords is None:
			return True
		newLines=[]
		COMMENT_ON=False

		for i,line in enumerate(lines):
			ret=self.lineParser(line,keywords)
			if isinstance(ret,str):
				line=ret
				KEYWORD_FOUND=None
			else:
				#print ret
				s, headStr, line=ret
				if len(headStr.strip())!=0 :
					newLines.append(headStr)
				KEYWORD_FOUND=True
				line="//"+line

			if ( COMMENT_ON or KEYWORD_FOUND) :
				if "{" in line:
					COMMENT_ON=True

				if "}" in line:
					COMMENT_ON=False
					slines=line.split("}")
					head=slines[0].replace("\n","\n//")
					tail=slines[1:]
					line="}".join([head]+tail)
				else:
					line=line.replace("\n","\n//")

			#line=line.strip()
			#if len(line)!=0:
			if len(line.strip())!=0 :
				newLines.append(line)
		header='#include "config.h"'
		fp=open(fMinName,"w")
		fp.write("%s\n%s"%(header,";".join(newLines)))
		fp.close()
		return True

def patchAll(patchDict):
	newPatchDict={}
	for key,value in list(patchDict.items()):
		#if not value:
		#	continue
		incName,incFile=key.split(":")
		print("*"*4,key,value)
		pat=patcher(incName,incFile,value)
		if  pat.patching():
			print("?"*4,key,value)
			newPatchDict[key]=value
	return newPatchDict
	
def genSwigI(patchDict):
	lines=open("tesseract.i.template").readlines()
	defines=[	"#define TESS_API\n",
				"#define TESS_LOCAL\n",
				"#define LEPT_DLL\n"]
	if not PYTHON3:
		defines.append("#define TESS_CAPI_INCLUDE_BASEAPI\n")
	a=list(defines)
	b=list(defines)
	for key,value in list(patchDict.items()):
		incName,incFile=key.split(":")
		
		if value:
			#b.append('%%include "%s_mini.h"\n'%incFile[:-2])
			#a.append('#include "%s_mini.h"\n'%incFile[:-2])
			b.append('%%include "%s"\n'%incFile)
			a.append('#include "%s"\n'%incFile)
		else:
			b.append('%%include "%s"\n'%incFile)
			a.append('#include "%s"\n'%incFile)
	a.append('#include "%s"\n'%"main.h")
	b.append('%%include "%s"\n'%"main.h")
	lines+=['\n%{\n']+a+['\n%}\n\n']
	lines+=['\n']+b+['\n']
	fp=open("tesseract.i","w")
	fp.write(''.join(lines))
	fp.close()


def run(tess_version):
	
	if not PYTHON3:
		patchDict=collections.OrderedDict([
			#(":config.h",None),
			("leptonica:allheaders.h",["setPixMemoryManager"]),
			("leptonica:pix.h",None),
			("tesseract:publictypes.h",["char* kPolyBlockNames"]),
			("tesseract:baseapi.h",["Dict", "ImageThresholder","GetUTF8Text"]),
			("tesseract:capi.h",["TessBaseAPIInit(","TessBaseAPISetFillLatticeFunc"]),
			("tesseract:pageiterator.h",None),
			("tesseract:ltrresultiterator.h",["ChoiceIterator"]),
			("tesseract:thresholder.h",None),
			("tesseract:resultiterator.h",None),
			("tesseract:renderer.h",None),
			#(":main.h",None),
			])
		if tess_version<"3.03":
			patchDict["tesseract:publictypes.h"].append("PageIterator")
			patchDict["tesseract:baseapi.h"]+=["iterator","PageIterator","GetLastInitLanguage"]
			patchDict["tesseract:ltrresultiterator.h"].append("PageIterator")
			del patchDict["tesseract:pageiterator.h"]
			del patchDict["tesseract:resultiterator.h"]
	else:
		patchDict=collections.OrderedDict([
			#(":config.h",None),
			#("leptonica:allheaders.h",["setPixMemoryManager"]),
			#("leptonica:pix.h",None),
			("tesseract:publictypes.h",["char* kPolyBlockNames","OcrEngineMode","PageIterator"]),
			("tesseract:baseapi.h",["Dict", "ImageThresholder","iterator"]),
			#("tesseract:capi.h",["TessBaseAPIInit(","TessBaseAPISetFillLatticeFunc"]),
			("tesseract:pageiterator.h",["PageIteratorLevel"]),
			("tesseract:ltrresultiterator.h",["ChoiceIterator","PageIterator"]),
			#("tesseract:thresholder.h",None),
			("tesseract:resultiterator.h",["PageIteratorLevel"]),
			#("tesseract:renderer.h",None),
			#(":main.h",None),
			])

	newPatchDict=patchAll(patchDict)
	#print newPatchDict
	#print "*"*50
	genSwigI(newPatchDict)


if __name__=="__main__":
	run("3.02")
