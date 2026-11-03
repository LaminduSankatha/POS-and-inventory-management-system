Disodi Stores POS — Kali Linux Guide

A local, offline-first Grocery Store Management \& Billing system(Python + Flask + SQLite). No internet needed for daily operation.No barcode scanner required.



This guide covers Kali Linux (also valid for Ubuntu/Debian/Mint).The same folder runs on Windows using run.bat — nothing in the appitself is OS-specific.



1\. What you need (one time)

Kali Linux (any recent version) with Python 3.10 or newer

check with: python3 --version

Internet connection once, for the first package install

The grocery\_store folder (copied from a Windows laptop or a USB stick)

2\. One-time installation

Open a terminal inside the grocery\_store folder(right-click in the folder → "Open Terminal Here", or cd to it):



\# 1. Install Python support packages if missing (usually already on Kali)sudo apt updatesudo apt install -y python3 python3-venv python3-pip# 2. Fix Windows line-endings if this folder came from a Windows PC#    (harmless on pure-Linux copies; REQUIRED after copying from Windows)sed -i 's/\\r$//' run.sh reset\_data.sh 2>/dev/null# 3. Make the launchers executable (one time)chmod +x run.shchmod +x reset\_data.sh 2>/dev/null# 4. Start it — this creates the private Python environment (venv),#    installs Flask/Pillow/openpyxl (needs internet ONCE), creates the#    database with sample data, and starts the server./run.sh

When you see Starting Disodi Stores POS..., open a browser at:



http://127.0.0.1:5000

From the next start onwards, everything runs fully offline.



3\. Daily use

Action	How

Start	./run.sh in the folder's terminal → browser at http://127.0.0.1:5000

Stop	Press Ctrl + C in that terminal

Log in (defaults)	admin / admin123 (Administrator) · cashier / cashier123 (Cashier)

Change passwords	Settings → My Password / User Accounts — do this before real use

The terminal that runs ./run.sh must stay open — it is the engine.Closing it stops the system.



4\. Where your data lives (all local, inside the folder)

Item	Location

Database (products, bills, settings, users)	database/grocery.db

Product photos	uploads/products/

Optional bulk-photo import folder	uploads/import\_photos/

Backups (timestamped copies)	backups/

Excel import/export	Products → Import from Excel (also exports in Reports)

The Sri Lanka clock (UTC+5:30) is built into the app, so Kali's owntimezone setting does not affect sales dates or "today's" figures.



5\. Feature quick reference

Billing/POS — instant search, category chips, Quick Sale buttons,+/− and typed quantities, discount, cash received \& change due,custom items not in the system, hold/resume bills

Stock — deducted automatically on Confirm, in one safe transaction;overselling blocked unless allowed in Settings

Receipts — Print (A4 or 80mm thermal mode), PNG image download,WhatsApp text share, copy text

Inventory — add/remove stock with reasons; every change recorded

Sales History — search, reprint, re-share; admin cancel/refundreturns stock and is excluded from totals

Reports — daily/weekly/monthly, best sellers, estimated profit,CSV export, Daily Closing

Excel import — Products → Import from Excel → Download Template

Reset tool — see section 6

6\. Reset tool on Linux (same options as Windows)

The reset tool is the same reset\_data.py used on Windows; only thelauncher differs. Options: (1) delete products+categories, (2) freshstart for real trading, (3) full factory reset, (4) delete ONLY saleshistory — keeps products, categories, stock, photos, users, settings.



Create reset\_data.sh if you don't have it yet:



\#!/usr/bin/env bashcd "$(dirname "$0")"venv/bin/python reset\_data.pyechoread -r -p "Press Enter to close..."

Then:



chmod +x reset\_data.sh./reset\_data.sh

Always: close the running app first (Ctrl + C), a backup is saved tobackups/ automatically before anything is deleted.



7\. Backups

Automatic: one backup per day, on the first app start of that day

Manual: Settings → Create Backup Now

Restore: stop the app (Ctrl + C), copy the wantedbackups/grocery\_backup\_...db over database/grocery.db(rename it to exactly grocery.db), start again

Keep a copy on a USB stick regularly — Settings also offersper-backup Download links

8\. Optional: use from other devices on the shop LAN

In the folder, create a file named .env containing:

HOST=0.0.0.0PORT=5000

Restart with ./run.sh; find this PC's IP with ipconfig-equivalent:ip a → look for the inet value of your Wi-Fi/LAN (e.g. 192.168.1.10)

Other laptops/phones on the SAME Wi-Fi open: http://192.168.1.10:5000

Never expose this app to the public internet. Default (no .env) binds to127.0.0.1 = this computer only, which is the safe state.



9\. Copying between a Windows laptop and Kali

The whole folder is portable — database, photos and settings included.



When copying FROM Windows TO Kali:



Delete the venv folder in the copy (it contains Windows binariesand cannot work on Linux — run.sh rebuilds it automatically)

Run the line-ending fix from section 2 step 2 (bash scripts withWindows line-endings fail with an error like $'\\r': command not found)

chmod +x run.sh and start

When copying FROM Kali TO Windows:



Delete the venv folder in the copy (run.bat rebuilds it)

Nothing else is needed

⚠️ Two copies do not sync. Pick ONE machine as the real billingmachine for the shop; treat copies as backup/emergency only.



10\. Troubleshooting (Kali)

./run.sh: Permission denied→ One-time: chmod +x run.sh



$'\\r': command not found or /bin/bash^M: bad interpreter→ The script has Windows line-endings (folder came from a Windows PC).→ Fix: sed -i 's/\\r$//' run.sh (and reset\_data.sh if present)



python3: command not found→ sudo apt install -y python3 python3-venv python3-pip



ensurepip is not available / venv creation fails→ sudo apt install -y python3-venv python3-pip, delete the brokenvenv folder (rm -rf venv), run ./run.sh again



error: externally-managed-environment during pip install→ You ran pip against the system Python. Don't: always start through./run.sh, which uses the project's own venv. If you created venvbefore installing python3-venv properly: rm -rf venv and retry.



Package install fails / times out→ Internet needed only for this step. Check connection, then rerun./run.sh — it resumes where it stopped.



Address already in use (port 5000 busy)→ Another copy of the app is already running (search your terminals),or stop it: pkill -f "python app.py".Or change the port: add PORT=5001 to .env, then browse tohttp://127.0.0.1:5001



sqlite3.OperationalError: database is locked / disk I/O error→ The app is open twice, or a reset tool ran while the app was up.Close ALL instances (Ctrl + C in every terminal running it,pkill -f "python app.py" if needed) and start one instance.



ModuleNotFoundError: No module named 'flask'→ The venv is missing or broken. rm -rf venv, then ./run.sh(rebuilds and reinstalls; needs internet once).



Browser doesn't open automatically→ Normal on some setups — open it yourself:http://127.0.0.1:5000



Page looks old after replacing files / after a reset→ Hard refresh: Ctrl + Shift + R (Linux equivalent of Ctrl + F5)



Photos won't upload (error about size)→ Upload limit is 20 MB and photos are auto-shrunk. If a photo stillfails, it's a format issue — use jpg/png/webp. Pillow must beinstalled (it is, via requirements.txt).



Excel import says support not installed→ openpyxl missing from the venv: make sure requirements.txtcontains openpyxl>=3.1, delete venv, rerun ./run.sh once online.Files must be .xlsx or .csv (old .xls: Save As → .xlsx in Excel).



Wrong "today" on the dashboard→ Shouldn't happen (Sri Lanka time is hardcoded). If you see it, an oldapp copy is running — restart.



Forgot admin password→ Option 3 of the reset tool restores default logins (wipes everythingelse too). Preferably another admin resets it in Settings instead.



11\. Quick command cheat-sheet

cd \~/path/to/grocery\_store   # go to the folder./run.sh                     # start the system (Ctrl + C to stop)ip a                         # find this PC's LAN IP (for other devices)pkill -f "python app.py"     # force-stop a stuck instancerm -rf venv                  # reset the Python environment (rebuilds on next start)venv/bin/python reset\_data.py  # reset tool without the .sh launcherls -lh database/ backups/    # check database \& backup sizes

12\. Security notes

Binds to 127.0.0.1 by default — other devices cannot reach it untilyou opt in with HOST=0.0.0.0 (LAN only, never the internet)

Passwords are stored hashed, never as plain text

Admin-only actions (prices, settings, cancels, resets) are enforcedserver-side; cashier accounts cannot touch them

Every destructive action saves a backup first

Two quick notes outside the file:



The line-endings fix (section 2, step 2) is the one I'd bet money on. You're constantly moving this folder between Windows machines and Kali, and Windows Notepad writes \\r\\n endings that make bash scripts fail with confusing errors. The sed one-liner in the README fixes it in a second — keep it handy.

If you hit a failure that's not in the troubleshooting table, copy the last few lines from the terminal running run.sh and send them here — same drill as on Windows, the terminal always names the real problem.

