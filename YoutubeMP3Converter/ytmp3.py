import yt_dlp

def youtube_to_audio(video_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path + '/%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            return "Download completed successfully"
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        result = youtube_to_audio(
            "https://www.youtube.com/watch?v=hWjwNgiLMgA",
            "/home/alexlu/Desktop/CodeSnippets/YoutubeMP3Converter/MP3Files/test.mp3"
        )
        print(result)
    except Exception as e:
        print(f"Failed to download: {str(e)}")