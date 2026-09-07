# 🎵 Apple Music Dedupe

## ℹ️ Overview

Apple Music dedupe is a simple tool to remove duplicate songs from a playlist. I developed this after accidentally pasting my playlist 4 times when switching to Apple Music only to realize later. After not being able to find a good way to remove the 3000 duplicate songs, I developed this script.

## 🚀 Usage


First export your Apple Music playlist, then just point the script to the exported xml file. 

<img src="https://raw.githubusercontent.com/Epic-Oreo/apple-music-dedupe/refs/heads/main/imgs/export.png" style="width:250px"/>

```bash
$ amdd myplaylist.xml out.xml
```


## ⬇️ Installation

```bash
$ uv tool install apple-music-dedupe
```