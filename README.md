### Youtube Downloader (ytdlr)

Just Another Front End for Pytube3 (JAFEFPT3)

This is a little tool that I have been meaning to write for a very long time. There are a multitude of sites out there that give you the ability to download audio and videos from YouTube.

I don't know what sits behind these web services. I also don't like the idea of downloading a random executable that may or may not
contain malicious code for the sake of grabbing a video or an audio track.

So with those thoughts in mind, I wanted to create something small for myself, with code that I can track. If anyone else finds this useful as I do, then great!

Let me know what else I can include or improve on.

Anyway, enough gum flappin'

## Dependencies

Ensure that you download the pytube3 package for this python script to work

pytube3

```
pip install pytube3
```

pillow
```
pip install pillow
```

requests
```
pip install requests
```

**NOTE**
There is currently a known issue with version available on pip, your best bet for getting pytube3 to run is below
```
pip3 uninstall -y pytube3
pip3 install git+https://github.com/nficano/pytube
```
