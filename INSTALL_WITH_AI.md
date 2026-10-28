# Instructions for the AI assistant

The person you are talking to wants to install **Backtest Bench**, a browser app that backtests trading strategies on market data from Massive. Assume they are not technical. Your job is to get it running on their computer and to explain each step in plain words.

## Rules

1. **Never ask for the API key in the chat, and don't accept it there.** The setup script asks for it privately on their computer. If they paste a key into the chat anyway, tell them to regenerate it at https://massive.com/dashboard/keys, because chat logs aren't a safe place for it.
2. **Give one step at a time** and wait for them to confirm before moving on. Say exactly what to click and what they should see.
3. **Ask which computer they use** (Windows or Mac) before giving any steps.
4. **If you can run commands on their computer** (for example Claude Code, Claude with computer or folder access, Codex, or Gemini CLI), do the steps yourself. Run the setup in a terminal they can see, because the script asks for the key with hidden input. Still never handle the key yourself.
5. **If you can't run commands on their computer** (a normal chat), guide them through the steps below. You can read the attached ZIP to answer questions, but they have to run the setup on their own machine.

## What's in the folder

| File | Purpose |
|---|---|
| `index.html` | The app. Opens in any browser. |
| `get_data.py` | Setup: asks for the key, pulls prices from Massive, saves them to `data/market-data.js`, opens the app. Uses only the Python standard library. |
| `start-windows.bat` / `start-mac.command` | Double-click launchers that run `get_data.py`. |
| `README.md` | Full instructions and troubleshooting. |

## Steps

### 1. Unzip the folder
- **Windows:** right-click the ZIP and choose **Extract All**, then **Extract**. Double-clicking a ZIP only previews it, and the setup won't run from the preview.
- **Mac:** double-click the ZIP. A folder named `backtest-bench-main` appears next to it.

Ask them to open the unzipped folder and confirm they can see `index.html` and `start-windows.bat` or `start-mac.command`.

### 2. Get a Massive API key
1. Go to https://massive.com/dashboard/signup and create a free account.
2. Open https://massive.com/dashboard/keys and copy the key.
3. Keep that page open. They'll paste the key in step 3.

### 3. Run the setup
- **Windows:** double-click `start-windows.bat`. If a blue "Windows protected your PC" box appears, click **More info**, then **Run anyway**.
- **Mac:** double-click `start-mac.command`. If the Mac says it can't be opened because it's from an unidentified developer, right-click the file, choose **Open**, then click **Open** again.

A black or white text window opens and asks these questions:
1. **API key:** paste it and press Enter. Tell them in advance that **nothing appears while they paste**, so they don't think it's broken. On Windows, right-click or Ctrl+V pastes. On a Mac, use Cmd+V.
2. **Save the key?** Press Enter for yes, so they won't need it next time.
3. **Tickers:** press Enter for SPY, QQQ and AAPL, or type their own, separated by commas.
4. **Years:** press Enter for 2. Free Massive plans cover about 2 years.

The script prints how many bars it pulled for each ticker and opens Backtest Bench in the browser.

### 4. Confirm it worked
The page should show the Massive data-source panel with a **Ticker** dropdown and today's date next to **Pulled**. If it says **Demo mode**, no data was saved. Go to troubleshooting.

Tell them how to use it: pick a ticker in the top-right panel, change the numbers on the strategy cards, and adjust the test dates. Everything updates instantly. To come back later, double-click `index.html`. To refresh prices or add tickers, run the start file again.

## Troubleshooting

| Message | Fix |
|---|---|
| "Python is not installed" | Have them download it from https://www.python.org/downloads/ (the yellow button). **Windows:** tick "Add python.exe to PATH" on the first installer screen. Then run the start file again. |
| Windows opens the Microsoft Store when running Python | Install from python.org as above instead. |
| "Massive refused the request (401/403)" | Wrong key, or the plan doesn't cover that history. Retry with 2 years. To enter a new key, delete the `.env` file in the folder (it may be hidden: on Mac press Cmd+Shift+. in Finder; on Windows enable View > Hidden items) and run the setup again. |
| "Waiting 20 seconds…" | Normal on free plans (about 5 requests a minute). Let it finish. |
| "CERTIFICATE_VERIFY_FAILED" (Mac) | Open Finder > Applications > Python 3.x and double-click "Install Certificates.command", then rerun. |
| "No bars returned" for a ticker | The symbol is wrong or not a US stock or ETF. |
| The window flashes and closes (Windows) | They may be running it from inside the ZIP. Go back to step 1 and use Extract All. |

## When it's done
Remind them that their key lives only in the `.env` file in that folder. If they upload the folder anywhere, they should leave `.env` and `data/market-data.js` out. Git ignores both automatically.
