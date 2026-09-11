from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    parsed_url = urlparse(url.strip())
    hostname = (parsed_url.hostname or "").lower()

    if hostname in {"youtu.be", "www.youtu.be"}:
        video_id = parsed_url.path.strip("/").split("/")[0]
    elif hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        video_id = parse_qs(parsed_url.query).get("v", [""])[0]
        if not video_id and parsed_url.path.startswith(("/shorts/", "/embed/")):
            video_id = parsed_url.path.split("/")[2]
    else:
        video_id = ""

    if not video_id:
        raise ValueError("Please enter a valid YouTube video URL.")

    return video_id

def get_full_transcript(url):
    video_id = extract_video_id(url)
    transcript_api = YouTubeTranscriptApi()
    transcripts = transcript_api.list(video_id)
    available_languages = [transcript.language_code for transcript in transcripts]

    if not available_languages:
        raise ValueError("This YouTube video does not have an available transcript.")

    preferred_languages = ["en"] if "en" in available_languages else available_languages
    transcript = transcript_api.fetch(video_id, languages=preferred_languages)

    full_text = " ".join([item.text for item in transcript])

    return full_text