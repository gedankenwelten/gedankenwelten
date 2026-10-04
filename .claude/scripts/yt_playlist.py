#!/usr/bin/env python3
"""
yt_playlist.py — Mac-natives YouTube-Playlist-Management (Schreibzugriff)

Schreibt direkt gegen die YouTube Data API v3 mit eigenem OAuth — ersetzt den
toten n8n-Webhook (abgelaufener OAuth). Lesen geht weiter Mac-nativ über yt-dlp;
DIESES Tool ist nur fürs Schreiben (add / remove / move) gedacht.

Zwei Konten (verschiedene Browser/Logins): jedes wird EINMAL autorisiert
(`auth <konto>` öffnet den Browser), danach liegt ein Refresh-Token lokal.

  Konten-Konvention:  <konto-1> · <konto-2>   (frei wählbar, nur ein Label fürs Token)

Ablage (außerhalb des Repos, gitignored):
  ~/.config/cortex-youtube/client_secret.json     <- Desktop-OAuth-Client (Google Cloud)
  ~/.config/cortex-youtube/token_<konto>.json     <- pro Konto, nach `auth`

Playlist-Argumente:  roher 18-stelliger ID-String, volle YouTube-URL,
                     ODER ein .env-Variablenname (z.B. <konto-1>_gedankenwelten_archiv).

Beispiele:
  yt_playlist.py auth <konto-1>
  yt_playlist.py list   <konto-1> <konto-1>_gedankenwelten_archiv
  yt_playlist.py add    <konto-1> <konto-1>_gedankenwelten_archiv RLfAqLny-_8
  yt_playlist.py move   <konto-1> <konto-1>_gedankenwelten <konto-1>_gedankenwelten_archiv RLfAqLny-_8
"""
import argparse, json, os, re, socket, sys
from pathlib import Path

# IPv4 bevorzugen: In manchen Netzen (Multipass/Fritzbox-Kollision, kaputte v6-Route)
# hängt httplib2 minutenlang am IPv6-Weg zu googleapis. IPv4-Adressen nach vorne
# sortieren — IPv6 bleibt als Fallback erhalten, wenn v4 fehlt.
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_first(host, *args, **kwargs):
    res = _orig_getaddrinfo(host, *args, **kwargs)
    return sorted(res, key=lambda r: 0 if r[0] == socket.AF_INET else 1)
socket.getaddrinfo = _ipv4_first

CFG = Path.home() / ".config" / "cortex-youtube"
CLIENT_SECRET = CFG / "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
ENV_PATH = Path("<vault>/.env")

# Quell-Playlisten („zu verarbeiten") und das Archiv („verarbeitet").
# cleanup/sweep halten die Quellen sauber: was archiviert ist, fliegt dort raus.
SOURCE_PLAYLISTS = [
    ("<konto-1>", "<konto-1>_gedankenwelten"),
    ("<konto-1>", "<konto-1>_gedankenwelten_global"),
    ("<konto-1>", "<konto-1>_republica"),
    ("<konto-2>", "<konto-2>_gedankenwelten"),
    ("<konto-2>", "<konto-2>_gedankenwelten_global"),
]
ARCHIVE_PLAYLIST = ("<konto-2>", "<konto-2>_gedankenwelten_archiv")


def _load_env():
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def resolve_playlist(arg, env):
    """ID-String, URL oder .env-Variablenname -> Playlist-ID."""
    if arg in env:
        arg = env[arg]
    m = re.search(r"[?&]list=([A-Za-z0-9_-]+)", arg)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{10,}", arg):
        return arg
    sys.exit(f"Konnte Playlist nicht auflösen: {arg!r}")


def token_path(account):
    return CFG / f"token_{account}.json"


def get_service(account, interactive=False):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    tp = token_path(account)
    creds = None
    if tp.exists():
        creds = Credentials.from_authorized_user_file(str(tp), SCOPES)
    if creds and creds.valid:
        pass
    elif creds and creds.expired and creds.refresh_token:
        from google.auth.exceptions import RefreshError
        try:
            creds.refresh(Request())
            tp.write_text(creds.to_json())
        except RefreshError:
            if not interactive:
                sys.exit(f"Token für '{account}' abgelaufen/widerrufen. Zuerst:  yt_playlist.py auth {account}")
            creds = None
    if creds and creds.valid:
        pass
    elif interactive:
        if not CLIENT_SECRET.exists():
            sys.exit(f"Fehlt: {CLIENT_SECRET}\n→ Desktop-OAuth-Client-JSON dorthin legen.")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
        creds = flow.run_local_server(
            port=0, access_type="offline", prompt="consent",
            open_browser=False,
            authorization_prompt_message=(
                "\n→ Öffne diese URL im RICHTIGEN Browser für Konto '%s'\n"
                "  (<konto-1> = Firefox, <konto-2> = Chrome) und stimme zu:\n\n  {url}\n" % account
            ),
            success_message="Fertig — du kannst das Browserfenster schließen.",
        )
        tp.write_text(creds.to_json())
        print(f"✓ Token gespeichert: {tp}")
    else:
        sys.exit(f"Kein gültiges Token für '{account}'. Zuerst:  yt_playlist.py auth {account}")
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def find_item_id(svc, playlist_id, video_id):
    """playlistItemId des Videos in der Playlist finden (für remove)."""
    page = None
    while True:
        resp = svc.playlistItems().list(
            part="snippet", playlistId=playlist_id, maxResults=50, pageToken=page
        ).execute()
        for it in resp.get("items", []):
            if it["snippet"]["resourceId"].get("videoId") == video_id:
                return it["id"]
        page = resp.get("nextPageToken")
        if not page:
            return None


def cmd_auth(args, env):
    get_service(args.account, interactive=True)


def cmd_list(args, env):
    svc = get_service(args.account)
    pid = resolve_playlist(args.playlist, env)
    page, n = None, 0
    while True:
        resp = svc.playlistItems().list(
            part="snippet", playlistId=pid, maxResults=50, pageToken=page
        ).execute()
        for it in resp.get("items", []):
            n += 1
            sn = it["snippet"]
            print(f"{n:3}. {sn['title'][:70]}  | {sn['resourceId'].get('videoId')}")
        page = resp.get("nextPageToken")
        if not page:
            break
    print(f"--- {n} Videos in {pid}")


def cmd_add(args, env):
    svc = get_service(args.account)
    pid = resolve_playlist(args.playlist, env)
    svc.playlistItems().insert(
        part="snippet",
        body={"snippet": {"playlistId": pid,
                          "resourceId": {"kind": "youtube#video", "videoId": args.video}}},
    ).execute()
    print(f"✓ {args.video} → Playlist {pid} hinzugefügt")


def cmd_remove(args, env):
    svc = get_service(args.account)
    pid = resolve_playlist(args.playlist, env)
    iid = find_item_id(svc, pid, args.video)
    if not iid:
        sys.exit(f"✗ {args.video} ist nicht in Playlist {pid}")
    svc.playlistItems().delete(id=iid).execute()
    print(f"✓ {args.video} aus Playlist {pid} entfernt")


def _all_items(svc, playlist_id):
    """Alle (itemId, videoId, title) einer Playlist."""
    out, page = [], None
    while True:
        resp = svc.playlistItems().list(
            part="snippet", playlistId=playlist_id, maxResults=50, pageToken=page
        ).execute()
        for it in resp.get("items", []):
            sn = it["snippet"]
            out.append((it["id"], sn["resourceId"].get("videoId"), sn.get("title", "")))
        page = resp.get("nextPageToken")
        if not page:
            return out


def cmd_cleanup(args, env):
    """Video aus ALLEN Quell-Playlisten entfernen + verifizieren (idempotent).

    Pipeline-Schritt 11b: nach der Note-Erstellung sicherstellen, dass das
    verarbeitete Video in keiner Quell-Liste mehr auftaucht.
    Exit 0 = Quellen sauber, Exit 1 = mind. ein Remove fehlgeschlagen.
    """
    import time
    services = {}
    failed = False
    for account, plname in SOURCE_PLAYLISTS:
        if account not in services:
            services[account] = get_service(account)
        svc = services[account]
        pid = resolve_playlist(plname, env)

        # Ein Video kann MEHRFACH in derselben Playlist stehen (Dubletten sind
        # bei YouTube erlaubt — die re:publica-Liste hatte einzelne Videos 4×).
        # Darum pro Durchgang ALLE Treffer einsammeln und löschen, nicht nur den
        # ersten; sonst meldet die Verifikation unten fälschlich einen Fehler.
        removed, err = 0, None
        for _ in range(3):                       # bis zu 3 Durchgänge
            iids = [iid for iid, vid, _ in _all_items(svc, pid) if vid == args.video]
            if not iids:
                break
            for iid in iids:
                try:
                    svc.playlistItems().delete(id=iid).execute()
                    removed += 1
                except Exception as e:
                    # 404 = schon weg (eventual consistency) → kein echter Fehler
                    if "404" in str(e) or "videoNotFound" in str(e):
                        continue
                    err = e
                    break
            if err:
                break
            time.sleep(3)                        # API ist eventual-consistent
        if err:
            print(f"✗ Remove aus {plname} fehlgeschlagen: {err}")
            failed = True
            continue
        if removed == 0:
            continue                             # war gar nicht drin
        extra = f" ({removed} Einträge — Dubletten)" if removed > 1 else ""
        print(f"✓ {args.video} aus {plname} entfernt{extra}")

        # Verifikation: ist es wirklich weg?
        gone = False
        for _ in range(3):
            time.sleep(3)
            if not find_item_id(svc, pid, args.video):
                gone = True
                break
        if not gone:
            print(f"✗ {args.video} steht immer noch in {plname}!")
            failed = True
    if failed:
        sys.exit(1)
    print(f"✓ Quell-Playlisten sauber — {args.video} in keiner Quelle mehr")


def cmd_dedupe(args, env):
    """Mehrfach eingetragene Videos einer Playlist auf je einen Eintrag reduzieren.

    YouTube erlaubt Dubletten in Playlists; sie entstehen leicht beim manuellen
    Sammeln. Behalten wird immer der **erste** Eintrag (Reihenfolge bleibt damit
    stabil), entfernt werden alle weiteren. --dry-run zeigt nur an.
    """
    svc = get_service(args.account)
    pid = resolve_playlist(args.playlist, env)
    items = _all_items(svc, pid)

    seen, surplus = set(), []
    for iid, vid, title in items:
        if vid in seen:
            surplus.append((iid, vid, title))
        else:
            seen.add(vid)

    print(f"{args.playlist}: {len(items)} Einträge, {len(seen)} eindeutige Videos, "
          f"{len(surplus)} überzählig")
    if not surplus:
        print("✓ keine Dubletten")
        return

    counts = {}
    for _, vid, title in surplus:
        counts.setdefault(vid, [title, 0])[1] += 1
    for vid, (title, n) in sorted(counts.items(), key=lambda x: -x[1][1]):
        print(f"    {n + 1}×  {title[:66]}  | {vid}")

    if args.dry_run:
        print("\n(dry-run — nichts entfernt)")
        return

    removed, failed = 0, 0
    for iid, vid, title in surplus:
        try:
            svc.playlistItems().delete(id=iid).execute()
            removed += 1
        except Exception as e:
            print(f"✗ {vid}: {e}")
            failed += 1
    print(f"\n✓ {removed} überzählige Einträge entfernt" + (f", {failed} fehlgeschlagen" if failed else ""))

    # Verifikation
    import time
    time.sleep(3)
    after = _all_items(svc, pid)
    uniq = len({vid for _, vid, _ in after})
    print(f"Kontrolle: {len(after)} Einträge, {uniq} eindeutige Videos")
    if len(after) != uniq:
        print("✗ es stehen weiterhin Dubletten in der Liste")
        sys.exit(1)


def cmd_sweep(args, env):
    """Alle bereits archivierten Videos aus den Quell-Playlisten räumen.

    Vergleicht das Archiv (<konto-2>_gedankenwelten_archiv) mit jeder Quell-Liste
    und entfernt dort alles, was schon archiviert ist. --dry-run zeigt nur an.
    """
    services = {}

    def svc_for(account):
        if account not in services:
            services[account] = get_service(account)
        return services[account]

    arc_account, arc_name = ARCHIVE_PLAYLIST
    arc_pid = resolve_playlist(arc_name, env)
    archived = {vid for _, vid, _ in _all_items(svc_for(arc_account), arc_pid) if vid}
    print(f"Archiv: {len(archived)} Videos in {arc_name}\n")

    total = 0
    for account, plname in SOURCE_PLAYLISTS:
        svc = svc_for(account)
        pid = resolve_playlist(plname, env)
        items = _all_items(svc, pid)
        stale = [(iid, vid, title) for iid, vid, title in items if vid in archived]
        print(f"— {plname}: {len(items)} Videos, davon {len(stale)} bereits archiviert")
        for iid, vid, title in stale:
            if args.dry_run:
                print(f"    [dry] {vid}  {title[:60]}")
            else:
                svc.playlistItems().delete(id=iid).execute()
                print(f"    ✓ entfernt: {vid}  {title[:60]}")
                total += 1
    if args.dry_run:
        print("\n(dry-run — nichts entfernt)")
    else:
        print(f"\n✓ Sweep fertig — {total} Videos aus den Quell-Listen geräumt")


def cmd_move(args, env):
    svc = get_service(args.account)
    src = resolve_playlist(args.src, env)
    dst = resolve_playlist(args.dst, env)
    # 1) ins Ziel hinzufügen (idempotent: doppelte ignorieren)
    try:
        svc.playlistItems().insert(
            part="snippet",
            body={"snippet": {"playlistId": dst,
                              "resourceId": {"kind": "youtube#video", "videoId": args.video}}},
        ).execute()
        print(f"✓ {args.video} → Ziel {dst} hinzugefügt")
    except Exception as e:
        print(f"… add übersprungen ({e})")
    # 2) aus Quelle entfernen
    iid = find_item_id(svc, src, args.video)
    if not iid:
        print(f"… {args.video} war nicht (mehr) in Quelle {src}")
    else:
        svc.playlistItems().delete(id=iid).execute()
        print(f"✓ {args.video} aus Quelle {src} entfernt")
    print("✓ move fertig")


def main():
    ap = argparse.ArgumentParser(description="Mac-natives YouTube-Playlist-Management (Schreibzugriff)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("auth"); a.add_argument("account"); a.set_defaults(fn=cmd_auth)
    l = sub.add_parser("list"); l.add_argument("account"); l.add_argument("playlist"); l.set_defaults(fn=cmd_list)
    ad = sub.add_parser("add"); ad.add_argument("account"); ad.add_argument("playlist"); ad.add_argument("video"); ad.set_defaults(fn=cmd_add)
    rm = sub.add_parser("remove"); rm.add_argument("account"); rm.add_argument("playlist"); rm.add_argument("video"); rm.set_defaults(fn=cmd_remove)
    cl = sub.add_parser("cleanup", help="Video aus allen Quell-Playlisten entfernen + verifizieren"); cl.add_argument("video"); cl.set_defaults(fn=cmd_cleanup)
    sw = sub.add_parser("sweep", help="alle archivierten Videos aus den Quell-Playlisten räumen"); sw.add_argument("--dry-run", action="store_true"); sw.set_defaults(fn=cmd_sweep)
    dd = sub.add_parser("dedupe", help="mehrfach eingetragene Videos einer Playlist auf einen Eintrag reduzieren")
    dd.add_argument("account"); dd.add_argument("playlist"); dd.add_argument("--dry-run", action="store_true"); dd.set_defaults(fn=cmd_dedupe)
    mv = sub.add_parser("move"); mv.add_argument("account"); mv.add_argument("src"); mv.add_argument("dst"); mv.add_argument("video"); mv.set_defaults(fn=cmd_move)

    args = ap.parse_args()
    args.fn(args, _load_env())


if __name__ == "__main__":
    main()
