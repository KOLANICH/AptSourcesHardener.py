import typing
import parglare
from pathlib import Path
import _io
import re
from collections import defaultdict
from pprint import pprint
import warnings
from urllib.parse import urlparse

import AptSourcesList

from fuckapt import trustedKeyringPath, trustedKeyringPartsPath
from fuckapt.machinery import getSigsInCaches


from .crypto import *


def createCachedSignatureFileNameForSourceDescriptor(el):
	parsedURI = urlparse(el.uri)
	splitted = [parsedURI.netloc]
	splitted.extend(filter(None, parsedURI.path.split("/")))
	splitted.append("dists")
	splitted.append(el.distribution)
	splitted.append("InRelease")
	return "_".join(splitted)

def generateHumanName(k):
	return "; ".join(u.uid for u in k.uids)


class Hardener():
	__slots__ = ("identifiedSigs", "tmpHome", "trustedKeysDir", "insecurePaths", "gpgContext")
	def __init__(self):
		self.identifiedSigs = None
		self.tmpHome = None
		self.trustedKeysDir = None
		self.insecurePaths = None
		self.gpgContext = None
	
	def identifySigs(self, lines):
		cachedSignatureFiles = getSigsInCaches()
		identifiedSigs = defaultdict(list)

		#pprint(cachedSignatureFiles)

		for el in lines:
			if isinstance(el, AptSourcesList.Record):
				fn = createCachedSignatureFileNameForSourceDescriptor(el)
				#print(el, fn, fn in cachedSignatureFiles)
				if fn in cachedSignatureFiles:
					identifiedSigs[cachedSignatureFiles[fn]].append(el)
		
		return identifiedSigs
	
	def mapFingerprintsToSecureKeysFilesAndSubkeys(self):
		trustedKeysDir = {}

		insecurePaths = defaultdict(set)

		def processKeyFile(kf):
			imps = self.gpgContext.key_import(kf.read_bytes())
			if isinstance(imps, str):
				raise Exception(imps, kf)
			for ik in imps.imports:
				k = self.gpgContext.get_key(ik.fpr)
				insecurity = isConsideredInsecure(k)
				if insecurity:
					warnings.warn("Key " + k.fpr + " ( " + generateHumanName(k) + " ) from " + str(kf) + " is considered insecure (" + str(insecurity) + ")!")
					insecurePaths[kf] |= {k.fpr}
				else:
					for sk in k.subkeys:
						trustedKeysDir[sk.fpr] = (kf, sk)

		processKeyFile(trustedKeyringPath)

		for kf in trustedKeyringPartsPath.glob("*.gpg"):
			processKeyFile(kf)
		for kf in trustedKeyringPartsPath.glob("*.asc"):
			processKeyFile(kf)

		processKeyFile(trustedKeyringPath)
		
		#pprint(trustedKeysDir)
		return trustedKeysDir, insecurePaths
	
	def __enter__(self):
		self.tmpHome = Path("./tmpKeyring").absolute()
		self.tmpHome.mkdir(parents=True, exist_ok=True)
		self.gpgContext = gpg.Context(armor=False, offline=True, home_dir=str(self.tmpHome))
		self.gpgContext.__enter__()
		self.trustedKeysDir, self.insecurePaths = self.mapFingerprintsToSecureKeysFilesAndSubkeys()
		print(self.trustedKeysDir)
		return self
	
	def __exit__(self, *args, **kwargs):
		self.gpgContext.__exit__(*args, **kwargs)

	def parseFile(self, ):
		return lines

	def __call__(self, fileToProcess: typing.Optional[typing.Union[Path, str]] = None):
		if fileToProcess is not None:
			fileToProcess = Path(fileToProcess)

		lines = list(AptSourcesList.parseSourceList(fileToProcess))
		
		identifiedSigs = self.identifySigs(lines)

		#pprint(identifiedSigs)

		for signatureFile, sourceDescriptors in identifiedSigs.items():
			verRes = self.gpgContext.verify(signatureFile.read_bytes())[1]
			#print(signatureFile, verRes)
			selectedKeyPath = None
			selectedKey = None
			for s in verRes.signatures:
				#print(signatureFile, s.fpr, s.fpr in self.trustedKeysDir)
				lookupResult = self.trustedKeysDir.get(s.fpr, None)
				if lookupResult is not None:
					candidateKeyFilePath, candidateKey = lookupResult
					if selectedKey is None or (selectedKey.timestamp < candidateKey.timestamp):  # todo: compare keys security
						selectedKeyPath = candidateKeyFilePath
						selectedKey = candidateKey

			if selectedKey is None:
				warnings.warn("Unable to find a suitable key in " + signatureFile)
				continue

			if selectedKeyPath in self.insecurePaths:
				warnings.warn("Selected key file " + str(selectedKeyPath) + " contains other keys that are insecure. So we will use hash!")
				selectedKeyPath = None

			for d in sourceDescriptors:
				if d.options is None:
					d.options = {}
				if "signed-by" not in d.options:
					if selectedKeyPath is not None and selectedKeyPath != trustedKeyringPath:
						d.options["signed-by"] = str(selectedKeyPath)
					else:
						d.options["signed-by"] = selectedKey.fpr
		return lines

