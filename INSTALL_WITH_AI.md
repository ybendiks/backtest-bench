# Instructions for the AI assistant

The person you are talking to wants to use **Backtest Bench**, a browser app that backtests trading strategies on market data from Massive. Assume they are not technical. There is nothing to install. Help them open the page and connect their Massive account.

## Rules

1. **Never ask for the API key in the chat, and don't accept it there.** It goes into the app's Connect box, which sends it only to Massive. If they paste a key into the chat anyway, tell them to regenerate it at https://massive.com/dashboard/keys.
2. **Give one step at a time** and wait for them to confirm before moving on.
3. **Ask whether they use Windows or a Mac** before step 1.
4. **If you can operate their computer**, you may unzip the folder and open `index.html` for them, but let them paste the key into the page themselves.
5. **Ignore `get_data.py`** unless they ask for a command-line setup. The page does everything on its own.

## Steps

1. **Unzip the download.**
   - Windows: right-click the ZIP, choose **Extract All**, then **Extract**.
   - Mac: double-click the ZIP.
2. **Open the app.** In the unzipped folder, double-click `index.html`. It opens in their web browser and shows simulated demo prices with a "Demo mode" note.
3. **Get a Massive API key** (skip if they have one). Sign up free at https://massive.com/dashboard/signup, then copy the key from https://massive.com/dashboard/keys.
4. **Connect.** In the **Data source** box at the top right of the app, paste the key, type the **Ticker to test** (SPY is filled in), and click **Connect and test**. The badge changes to **Connected** and the results load.
5. **Test other tickers.** Type a symbol such as `NVDA` in **Ticker to test** and click **Test**. Pulled tickers appear under **Your tickers**. Click one to switch back to it.
6. **Explore.** The numbers on each strategy card change its rules. The test dates under the cards narrow the test. **History from / To** with **Update all** pulls a different date range from Massive.

Next time, they just double-click `index.html`. Their key and tickers are remembered in that browser.

## Troubleshooting

| Message in the app | Fix |
|---|---|
| "Massive didn't accept this API key" | Copy the key again from the keys page. Watch for a missing first or last character. |
| "Massive declined the request" | Their plan doesn't cover the dates. Free plans cover about 2 years, so set **History from** later and click **Update all**. |
| "Trying again in 20s…" | Normal on free plans (about 5 requests a minute). Wait. |
| "No usable data for XYZ" | Wrong symbol, or not a US stock or ETF. |
| "Your browser couldn't reach Massive" | Internet or office network issue. Try another network. |
| The page opened but looks unstyled or empty | They may have opened it from inside the ZIP preview. Extract first (step 1). |
