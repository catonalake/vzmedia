hls_master_head = """#EXTM3U
#EXT-X-VERSION:{hls_version}
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="aac",NAME="English",LANGUAGE="en",AUTOSELECT=YES,DEFAULT=YES"""

hls_master_ray = """#EXT-X-STREAM-INF:PROGRAM-ID=1,AUDIO="aac",CODECS="mp4a.40.5,avc1.42000c",FRAME-RATE={fps:.2f},RESOLUTION={w}x{h},BANDWIDTH={peak_bps},AVERAGE-BANDWIDTH={avg_bps},"""

hls_master_ifo_ray = """#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={w}x{h},CODECS="avc1.4d001f",URI="{uri}"""

hls_media_head = """#EXTM3U
#EXT-X-TARGETDURATION:{max_segment_duration}
#EXT-X-VERSION:{hls_version}
#EXT-X-PLAYLIST-TYPE:VOD
#EXT-X-MEDIA-SEQUENCE:0"""

hls_master_sub="""#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",NAME="{name}",AUTOSELECT=YES,DEFAULT=YES,FORCED=YES,LANGUAGE="{language}","""
