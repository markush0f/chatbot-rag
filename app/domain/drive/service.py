from __future__ import annotations
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


class DriveService:
    def __init__(self):
        self.creds = None
        self.service = self._load_service()

    def _load_service(self):
        creds_path = "credentials.json"
        token_path = "token.pickle"

        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(token_path, "wb") as token:
                pickle.dump(self.creds, token)

        return build("drive", "v3", credentials=self.creds)

    def list_files(self, mime_filters: list[str] | None = None) -> list[dict]:
        """
        Lista archivos del Drive (PDF, DOCX, TXT, etc.)
        """
        query = (
            " or ".join([f"mimeType='{m}'" for m in mime_filters])
            if mime_filters
            else None
        )

        results = (
            self.service.files()
            .list(q=query, fields="files(id, name, mimeType, modifiedTime, size)")
            .execute()
        )

        files = results.get("files", [])
        return [
            {
                "id": f["id"],
                "name": f["name"],
                "mimeType": f["mimeType"],
                "size": f.get("size", "—"),
                "modified": f.get("modifiedTime", ""),
            }
            for f in files
        ]
