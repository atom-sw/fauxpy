# import glob
# import os
# import shutil
from pathlib import Path

# from typing import List

# import pathlib


def getDataPath(directoryName: str, fileName: str) -> Path:
    thisFile = Path(__file__)
    thisDir = thisFile.parent
    dataDir = thisDir / "data"
    return dataDir / directoryName / fileName


# def deleteNoise(projectPath: Path):
#     filesToRemove = [
#         "instrumentationCollectModeExecutedPredicateSequence.txt",
#         "instrumentationCollectModeConfig.txt",
#         "instrumentationCollectModeEvaluationCounter.txt",
#     ]
#
#     for item in filesToRemove:
#         pathItem = projectPath / pathlib.Path(item)
#         if pathItem.exists():
#             pathItem.unlink()
#
#     dirToRemove = projectPath / "FauxPyCollectModeReport"
#     if dirToRemove.exists():
#         shutil.rmtree(dirToRemove)
#
#     reportDirsToRemove = projectPath.parent.rglob("FauxPyReport*")
#     for item in reportDirsToRemove:
#         shutil.rmtree(item)
#
#     pattern = f"{str(projectPath.absolute())}/**/*.pyc"
#     fileList = glob.glob(pattern, recursive=True)
#     for filePath in fileList:
#         if os.path.exists(filePath):
#             os.remove(filePath)


# def runCommand(command: List[str], workingDir: str):
#     import subprocess
#
#     execOut = subprocess.run(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         universal_newlines=True,
#         cwd=workingDir,
#     )
#
#     print(execOut.stdout)
#     print(execOut.stderr)
