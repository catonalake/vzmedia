# Welcome
Hello, and thanks for taking the time to work on our code exercise. We hope you find it both interesting and challenging.

## Setup
This code runs in Python 3, so you'll want to be able to execute that. Most Python projects use virtualenvironments to keep their Python dependencies separated.

To get the code up and running:
 1. Install Pip via the instructions at <https://pip.pypa.io/en/stable/installing/>
 1. run `pip install -r requirements.txt` to install the Python dependencies.
 1. run `python app.py` to start the application. By default, it runs at `0.0.0.0:8080`.
 
 Hooray, you have a working HLS manifest-generating server running locally on port 8080. If you have an HLS player you're familiar with, you can tell it to play `http://localhost:8080/hls/vod/d7415eeeb78a4aca9ce6e10735ddd76b.m3u8` and it should. 
 
 If you're not familiar with any HLS players, paste the above .m3u8 URL into the "File URL" field on [JW Player's stream tester](http://demo.jwplayer.com/developer-tools/http-stream-tester/).
 
 You should get video playback. If not, something's wrong. Please feel free to ask questions about setup if anything is unclear at all. 
 
 ## HLS Background
 This small repo implements a very basic HLS (HTTP Live Streaming) manifest generator. You can read the HLS spec at <http://tools.ietf.org/html/draft-pantos-http-live-streaming> (you are not required to read and digest the entire spec, but you may find it a useful reference).
 
 Briefly, HLS specifies a couple of things you must do to create a valid stream:
 1. Break your source video into chunks
 2. Encode each chunk at a number of different bitrates/resolutions. Upload these segments to a location where they're accessible via HTTP.
 3. For each bitrate/resolution, create a media playlist that lists the URLs of each of the video segments of that bitrate/resolution in the order they're to be played. Upload this list to an HTTP-accessible location.
 4. Create a master playlist that contains the URLs of each of the media playlists from the previous step. Upload this master playlist to an HTTP-accessible location. The URL for the master playlist is the URL for your video stream.
 
 An HLS-compatible client will be capable of taking the master playlist URL and displaying the video stream it describes.
 
 # Exercise Tasks:
 1. This folder is a Git repo. Create a new branch, and commit your work to the new branch as you perform the following tasks. When you've completed all the tasks, re-zip up the folder and send it back.

 2. Customers report that playback works for asset `d7415eeeb78a4aca9ce6e10735ddd76b` but returns an HTTP 500 error for asset `9c498f15770c4f189f7b9b862ce98f88`. Please fix this bug.
 
 3. Return an HTTP 404 (instead of 500) response to requests for the master playlist of an `asset_id` that doesn't exist. Do the same for media playlists.
 
 4. Customers are requesting the ability to specify which media playlists (Verizon Media calls these "rays") are listed in the Master playlist generated by the `/hls/vod/{asset_id}.m3u8` endpoint. Add support for a query string parameter that specifies which 'rays' will be returned in the Master playlist.
 
 5. Customers report that the subtitles for asset `d7415eeeb78a4aca9ce6e10735ddd76b` aren't showing up in the master playlist. These are added via the `EXT-X-MEDIA:TYPE=SUBTITLES` tag (see [section 4.3.4.1 of the HLS spec](https://tools.ietf.org/html/rfc8216#section-4.3.4.1)).
 
     Update the Master Playlist generation code to include these tags for assets which have subtitles. The URI value for these tags follows the same pattern as the media manifest URLs.
     
     When done correctly, the UI for most players (including the JW test player linked above) should offer the ability to turn on subtitles/closed-captions. The first captions for asset `d7415eeeb78a4aca9ce6e10735ddd76b` appear 23 seconds from the beginning.
 