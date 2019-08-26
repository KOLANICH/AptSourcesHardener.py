from pathlib import Path
from plumbum import cli

from . import *


class HardenerCLI(cli.Application):
	def main(self, fileToProcess=None):
		with Hardener() as h:
			for el in h():
				print(str(el))

if __name__ == "__main__":
	HardenerCLI.run()
