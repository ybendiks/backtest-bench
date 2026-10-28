#!/usr/bin/env python3
"""Optional: pre-load Backtest Bench with daily bars from Massive from the command line.

Most people don't need this. Open index.html and use the Connect box in the
page instead. This script is for scripted or offline setups.

Run it with no arguments and it asks you everything it needs:
    python get_data.py            (Windows: py get_data.py)
    python3 get_data.py           (Mac / Linux)

Or pass options:
    python get_data.py --tickers SPY,QQQ,AAPL --years 2

Your API key is read from the MASSIVE_API_KEY environment variable or from a
.env file in this folder. If neither exists, the script asks for it and can
save it to .env (which is never uploaded to GitHub). Only the Python standard
library is used, so there is nothing to install.
"""
import argparse
import datetime as dt
import getpass
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

HERE = pathlib.Path(__file__).resolve().parent
ENV_FILE = HERE / ".env"
OUT_FILE = HERE / "data" / "market-data.js"
APP_FILE = HERE / "index.html"
API = "https://api.massive.com"
DEFAULT_TICKERS = "SPY,QQQ,AAPL"


def say(msg=""):
    print(msg, flush=True)


def read_env_key():
    if not ENV_FILE.exists():
        return ""
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("MASSIVE_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def get_key(interactive):
    key = os.environ.get("MASSIVE_API_KEY", "").strip()
    if key:
        say("Using the API key from your MASSIVE_API_KEY environment variable.")
        return key
    key = read_env_key()
    if key:
        say("Using the API key saved in this folder's .env file.")
        return key
    if not interactive:
        sys.exit("No API key found. Set MASSIVE_API_KEY or create a .env file (see .env.example).")
    say("You need a free Massive API key.")
    say("  1. Sign up at https://massive.com/dashboard/signup")
    say("  2. Copy your key from https://massive.com/dashboard/keys")
    say()
    say("Paste the key below and press Enter. Nothing will show on screen while")
    say("you paste. That's normal; it keeps the key private.")
    key = getpass.getpass("API key: ").strip()
    if not key:
        sys.exit("No key entered. Run the setup again when you have one.")
    answer = input("Save the key in this folder so you don't have to paste it next time? [Y/n] ").strip().lower()
    if answer in ("", "y", "yes"):
        ENV_FILE.write_text(f"MASSIVE_API_KEY={key}\n", encoding="utf-8")
        say("Saved to .env in this folder. It is never uploaded to GitHub.")
    return key


def request_json(url, key):
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(url + sep + "apiKey=" + urllib.parse.quote(key),
                                 headers={"User-Agent": "backtest-bench/1.0"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 5:
                say("  Massive's rate limit was reached. Waiting 20 seconds, then trying again…")
                time.sleep(20)
                continue
            if e.code in (401, 403):
                raise SystemExit(
                    f"Massive refused the request ({e.code}). Either the API key is wrong, or your plan "
                    "doesn't cover this date range. Try fewer years (free plans cover about 2), or delete "
                    "the .env file in this folder and run the setup again to enter a new key.")
            raise SystemExit(f"Massive returned an error ({e.code}). Try again in a minute.")
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if "CERTIFICATE_VERIFY_FAILED" in reason:
                raise SystemExit(
                    "Python couldn't verify Massive's security certificate. On a Mac, open "
                    "Applications > Python 3.x and double-click 'Install Certificates.command', "
                    "then run the setup again.")
            raise SystemExit(f"Couldn't reach Massive ({reason}). Check your internet connection.")
    raise SystemExit("Massive kept rate-limiting the requests. Wait a minute and try again.")


def fetch_bars(ticker, start, end, key):
    path = f"/v2/aggs/ticker/{urllib.parse.quote(ticker)}/range/1/day/{start}/{end}"
    url = API + path + "?" + urllib.parse.urlencode({"adjusted": "true", "sort": "asc", "limit": 50000})
    bars = []
    while url:
        data = request_json(url, key)
        for b in data.get("results") or []:
            bars.append([int(b["t"]), b["o"], b["h"], b["l"], b["c"]])
        url = data.get("next_url")
    return bars, f"GET {path}"


def main():
    ap = argparse.ArgumentParser(description="Pull daily bars from Massive for Backtest Bench.")
    ap.add_argument("--tickers", help=f"Comma-separated tickers (default {DEFAULT_TICKERS})")
    ap.add_argument("--years", type=float, help="Years of history to pull (default 2)")
    ap.add_argument("--no-open", action="store_true", help="Don't open the app when done")
    args = ap.parse_args()
    interactive = sys.stdin.isatty() and not (args.tickers or args.years)

    say("=" * 60)
    say(" Backtest Bench setup: pulling market data from Massive")
    say("=" * 60)
    key = get_key(sys.stdin.isatty())

    tickers = args.tickers
    years = args.years
    if interactive:
        say()
        tickers = input(f"Which tickers? Separate with commas, or press Enter for {DEFAULT_TICKERS}: ").strip()
        y = input("How many years of history? Press Enter for 2 (the free plan's limit): ").strip()
        try:
            years = float(y) if y else None
        except ValueError:
            years = None
    tickers = [t.strip().upper() for t in (tickers or DEFAULT_TICKERS).split(",") if t.strip()]
    years = years or 2

    end = dt.date.today()
    start = end - dt.timedelta(days=int(round(years * 365)))
    say()
    say(f"Pulling {', '.join(tickers)} from {start} to {end}…")

    out = {"source": "Massive Stocks REST API", "adjusted": True,
           "pulled": end.isoformat(), "tickers": {}}
    for t in tickers:
        bars, endpoint = fetch_bars(t, start.isoformat(), end.isoformat(), key)
        if not bars:
            say(f"  {t}: no bars returned. Check the ticker symbol. Skipped.")
            continue
        out["tickers"][t] = {"endpoint": endpoint, "bars": bars}
        say(f"  {t}: {len(bars)} daily bars")

    if not out["tickers"]:
        sys.exit("No data was downloaded, so nothing was saved.")

    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text("window.MASSIVE_DATA = " + json.dumps(out, separators=(",", ":")) + ";\n",
                        encoding="utf-8")
    say()
    say(f"Saved {len(out['tickers'])} ticker(s) to data/market-data.js")
    if not args.no_open:
        say("Opening Backtest Bench in your browser…")
        webbrowser.open(APP_FILE.as_uri())
    say("Done. To see it again later, double-click index.html in this folder.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        say("\nStopped.")
