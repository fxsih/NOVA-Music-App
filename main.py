from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import os

app = FastAPI()

MUSIC_DIR = "music_library"

@app.get("/songs")
def list_songs():
    """List all available songs."""
    try:
        songs = os.listdir(MUSIC_DIR)
        return {"songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream/{song_name}")
def stream_song(song_name: str):
    """Stream a song instead of downloading it."""
    song_path = os.path.join(MUSIC_DIR, song_name)

    if not os.path.exists(song_path):
        raise HTTPException(status_code=404, detail="Song not found")

    def iterfile():
        with open(song_path, mode="rb") as file:
            yield from file

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
