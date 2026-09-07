import typer
from pathlib import Path
from typing import Annotated
import xml.etree.ElementTree as ET
from rich import print


app = typer.Typer()

def validateKeyValue(dict: ET.Element[str]):
  # 0 = key, 1 = value
  last = 1
  for subElement in dict:
    if last == 1 and subElement.tag == "key":
      last = 0
    elif last == 0 and subElement.tag != "key":
      last = 1
    else:
      print("Key Value validation failed!")
      raise typer.Abort()


def getKey(dict: ET.Element[str], key: str):
  next = False
  for subElement in dict:
    if next:
      return subElement
    if subElement.tag == "key" and subElement.text == key:
      next = True

  print("Key not found!")
  raise typer.Abort()


def findPlaylist(playlists: ET.Element[str], search: str):
  for playlist in playlists:
      if getKey(playlist, "Name").text == search or getKey(playlist, "Playlist ID").text == search:
        return playlist

  raise typer.BadParameter("Playlist not found!")

def dedupe(target: Path, output: Path, targetPlaylist: str):
  tree = ET.parse(target)
  root = tree.getroot()
  rootDict = root.find("dict")
  if rootDict == None:
    print("Failed to find root Dict")
    raise typer.Abort()

  validateKeyValue(rootDict)


  playlists = getKey(rootDict, "Playlists").findall("dict")
  if len(playlists) == 0:
    print("[red underline]No playlists found in xml file!\n")
    raise typer.Abort()
  if len(playlists) > 1:
    print("[red underline]More then one playlist in file! make sure you are exporting only one playlist and not your entire library!\n")
    raise typer.Abort()

  playlist = playlists[0]

  foundIds = []
  foundDuplicates = []
  dupes = 0
  total = 0

  print(f"Reading playlist: [bright_blue underline]{getKey(playlist, "Name").text}")
  items = getKey(playlist, "Playlist Items")

  for item in items:
    trackID = getKey(item, "Track ID").text
    total += 1

    if trackID not in foundIds:
      foundIds.append(trackID)
    else:
      foundDuplicates.append(item)
      dupes += 1


  for item in foundDuplicates:
    items.remove(item)

  print(f"Total: [bright_blue  underline]{total}")
  print(f"Dupes: [red  underline]{dupes}")

  tree.write(output.absolute())

  with open(output.absolute(), "r+") as file:
    content = file.read()
    file.seek(0)
    file.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">''' + content)

  print("Completed!")


@app.command()
def main(target: Path, output: Path, playlist: Annotated[str, typer.Argument(help="The name or id of the target playlist")]):

  if target is None:
    raise typer.BadParameter("No file specified!")
  elif target.is_file():
    dedupe(target, output, playlist)
  elif target.is_dir():
    raise typer.BadParameter("Directories not supported!")
  elif not target.exists():
    raise typer.BadParameter("File does not exist!")
