"""ReelPipe's API: it hands out upload URLs and reports each video's status.

Run it from reelpipe/ in Git Bash (task 8, step 10):
    uv run --env-file .env fastapi dev api/app/main.py
Then open http://localhost:8000/docs to try each route.

Every route below is a stub. Until you write it, it answers 500, and the API's log shows
NotImplementedError with the number of the task that writes it.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="ReelPipe")

# The web app runs on http://localhost:5173 and calls this API from the browser, as in P4.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class UploadRequest(BaseModel):
    """What the web app sends to POST /uploads before it uploads the file itself."""

    filename: str
    content_type: str  # for example "video/mp4"
    size: int  # in bytes


class UploadResponse(BaseModel):
    """What POST /uploads returns: where the browser uploads the file, and how."""

    video_id: str
    upload_url: str
    headers: dict[str, str]  # the browser sends these headers with its PUT, unchanged


@app.post("/uploads")
def create_upload(upload: UploadRequest) -> UploadResponse:
    """Hand out a presigned PUT URL for one new video (task 8, steps 6 to 8).

    - Refuse with 422 if content_type does not start with "video/" or size is over 100 MB.
    - Make video_id with uuid4().hex.
    - Sign a PUT for the key uploads/<video_id> that expires in 600 seconds, with the content type signed.
    - Return the video_id, the upload_url and the headers the browser must send.
    The video's bytes never come to the API: the browser sends them straight to the bucket.

    TODO(task 19): sign through get_backend().presign_upload(...) instead of calling boto3 here.
    """
    raise NotImplementedError("TODO(task 8): check the file, then sign a PUT URL for uploads/<video_id>")


@app.post("/uploads/{video_id}/complete", status_code=202)
def complete_upload(video_id: str) -> dict:
    """The web app calls this after its PUT has finished (task 9, step 4).

    - Check that uploads/<video_id> exists (head_object). If it does not, answer 404.
    - Write status "uploaded" with app.status, then send one job with app.jobs.send_job.
    - Answer 202.

    TODO(task 18): read JOB_TRIGGER (default "api"). With JOB_TRIGGER=event, only return the status,
        because the Lambda function writes "uploaded" and sends the job.
    TODO(task 19): check the upload with get_backend().list("uploads/<video_id>") instead of head_object.
    """
    raise NotImplementedError("TODO(task 9): check the upload, record 'uploaded', then send one job")


@app.get("/videos")
def list_videos() -> list[dict]:
    """Every video's status record, read from status/, newest first (task 9, step 5)."""
    raise NotImplementedError("TODO(task 9): return every status record, newest first")


@app.get("/videos/{video_id}")
def get_video(video_id: str) -> dict:
    """One video's status record, or 404 if it has none (task 9, step 5)."""
    raise NotImplementedError("TODO(task 9): return this video's status record, or answer 404")
