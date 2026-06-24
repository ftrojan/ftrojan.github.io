#!/usr/bin/env python3
"""
Upload generated posters to Google Drive and update events.json poster_id values.

Drive layout:
  events/                          (folder id below)
    2025-07-24/
      poster_2025-07-24.png

poster_id in events.json is the Google Drive file id used by the site:
  https://lh3.googleusercontent.com/d/{poster_id}

Setup (one-time):
  1. Create an OAuth 2.0 Desktop client in Google Cloud Console.
  2. Enable the Google Drive API for the project.
  3. Save the client JSON as scripts/credentials.json
  4. Run this script; a browser opens for consent on first use.
     Token is cached in scripts/token.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

REPO_ROOT = Path(__file__).resolve().parents[1]
EVENTS_PATH = REPO_ROOT / "src/assets/events.json"
POSTERS_DIR = REPO_ROOT / "posters"
SCRIPTS_DIR = Path(__file__).resolve().parent
CREDENTIALS_PATH = SCRIPTS_DIR / "credentials.json"
TOKEN_PATH = SCRIPTS_DIR / "token.json"

EVENTS_FOLDER_ID = "1HY_rmBa0PGE6VqpNZrjy3w2YQdgjS099"
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_MIME = "application/vnd.google-apps.folder"


def needs_poster(event: dict) -> bool:
    return event.get("poster_id") is None


def poster_filename(event_date: str) -> str:
    return f"poster_{event_date}.png"


def get_drive_service():
    creds = None
    if TOKEN_PATH.is_file():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), DRIVE_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.is_file():
                print(
                    f"Missing OAuth credentials at {CREDENTIALS_PATH}.\n"
                    "Download a Desktop OAuth client JSON from Google Cloud Console "
                    "and save it as scripts/credentials.json.",
                    file=sys.stderr,
                )
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), DRIVE_SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    return build("drive", "v3", credentials=creds)


def find_child_by_name(service, parent_id: str, name: str, mime_type: str | None = None) -> str | None:
    query_parts = [
        f"'{parent_id}' in parents",
        f"name = '{name}'",
        "trashed = false",
    ]
    if mime_type:
        query_parts.append(f"mimeType = '{mime_type}'")

    response = (
        service.files()
        .list(
            q=" and ".join(query_parts),
            fields="files(id, name)",
            pageSize=10,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )
    files = response.get("files", [])
    return files[0]["id"] if files else None


def ensure_folder(service, parent_id: str, name: str, dry_run: bool) -> str:
    folder_id = find_child_by_name(service, parent_id, name, FOLDER_MIME)
    if folder_id:
        return folder_id

    if dry_run:
        print(f"[dry-run] Would create folder {name}")
        return f"dry-run-folder-{name}"

    created = (
        service.files()
        .create(
            body={
                "name": name,
                "mimeType": FOLDER_MIME,
                "parents": [parent_id],
            },
            fields="id",
            supportsAllDrives=True,
        )
        .execute()
    )
    print(f"Created folder {name}")
    return created["id"]


def ensure_poster_file(
    service,
    folder_id: str,
    local_path: Path,
    filename: str,
    dry_run: bool,
) -> str:
    existing_id = find_child_by_name(service, folder_id, filename)
    if existing_id:
        print(f"Found existing {filename} -> {existing_id}")
        return existing_id

    if dry_run:
        print(f"[dry-run] Would upload {local_path} as {filename}")
        return f"dry-run-file-{filename}"

    media = MediaFileUpload(str(local_path), mimetype="image/png", resumable=True)
    created = (
        service.files()
        .create(
            body={"name": filename, "parents": [folder_id]},
            media_body=media,
            fields="id",
            supportsAllDrives=True,
        )
        .execute()
    )
    file_id = created["id"]
    print(f"Uploaded {filename} -> {file_id}")
    return file_id


def sync_event_poster(service, event: dict, dry_run: bool) -> str | None:
    event_date = event["date"]
    filename = poster_filename(event_date)
    local_path = POSTERS_DIR / filename

    if not local_path.is_file():
        print(f"Skipping {event_date}: local poster not found at {local_path}", file=sys.stderr)
        return None

    folder_id = ensure_folder(service, EVENTS_FOLDER_ID, event_date, dry_run)
    return ensure_poster_file(service, folder_id, local_path, filename, dry_run)


def update_events_json(events: list[dict], updates: dict[str, str], dry_run: bool) -> bool:
    if not updates:
        return False

    for event in events:
        event_date = event["date"]
        if event_date in updates:
            event["poster_id"] = updates[event_date]

    if dry_run:
        for event_date, file_id in updates.items():
            print(f"[dry-run] Would set poster_id for {event_date} -> {file_id}")
        return False

    EVENTS_PATH.write_text(
        json.dumps(events, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {EVENTS_PATH.relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload posters to Google Drive and update events.json."
    )
    parser.add_argument(
        "--date",
        help="Sync only this event date (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show actions without uploading or editing events.json.",
    )
    args = parser.parse_args()

    if not EVENTS_PATH.is_file():
        print(f"Events file not found: {EVENTS_PATH}", file=sys.stderr)
        return 1

    events = json.loads(EVENTS_PATH.read_text(encoding="utf-8"))
    pending = [event for event in events if needs_poster(event)]

    if args.date:
        pending = [event for event in pending if event["date"] == args.date]
        if not pending:
            print(f"No event without poster_id found for date {args.date}.", file=sys.stderr)
            return 1

    if not pending:
        print("No events without poster_id found.")
        return 0

    service = get_drive_service()
    if service is None:
        return 1

    updates: dict[str, str] = {}
    for event in pending:
        event_date = event["date"]
        print(f"Processing {event_date}...")
        file_id = sync_event_poster(service, event, args.dry_run)
        if file_id and not file_id.startswith("dry-run-"):
            updates[event_date] = file_id
        elif file_id and args.dry_run:
            updates[event_date] = f"dry-run-{event_date}"

    if args.dry_run:
        update_events_json(events, updates, dry_run=True)
        print("Dry run complete.")
        return 0

    if update_events_json(events, updates, dry_run=False):
        print(f"Done. Updated {len(updates)} event(s).")
    else:
        print("No events.json changes were written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
