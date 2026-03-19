#!/bin/bash
# setup_reminders.sh — Set up daily prep reminders on macOS
# Run once: bash setup_reminders.sh
# To remove:  bash setup_reminders.sh --remove

SCRIPT="/Users/jayanti/Documents/dev/senior-prep/prep.py"
PYTHON="/usr/bin/python3"
PLIST_DIR="$HOME/Library/LaunchAgents"
LOG_DIR="/Users/jayanti/Documents/dev/senior-prep/logs"

MORNING_LABEL="com.preptracker.morning"
EVENING_LABEL="com.preptracker.evening"
WEEKLY_LABEL="com.preptracker.weekly"
TERMINAL_LABEL="com.preptracker.terminal"

# ── Remove mode ───────────────────────────────────────────────────────────────
if [ "$1" = "--remove" ]; then
    echo "Removing prep reminders..."
    for label in $MORNING_LABEL $EVENING_LABEL $WEEKLY_LABEL; do
        launchctl unload "$PLIST_DIR/${label}.plist" 2>/dev/null
        rm -f "$PLIST_DIR/${label}.plist"
        echo "  Removed: $label"
    done
    # Remove terminal hook from .zshrc
    sed -i '' '/prep.py.*notify.*terminal/d' ~/.zshrc 2>/dev/null
    echo "Done. All reminders removed."
    exit 0
fi

# ── Setup mode ────────────────────────────────────────────────────────────────
echo ""
echo "Setting up SDE Prep Reminders..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p "$PLIST_DIR" "$LOG_DIR"

# ── 1. Morning reminder — 6:00 AM daily ───────────────────────────────────────
cat > "$PLIST_DIR/${MORNING_LABEL}.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${MORNING_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON}</string>
        <string>${SCRIPT}</string>
        <string>notify</string>
        <string>morning</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>   <integer>6</integer>
        <key>Minute</key> <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/notify_morning.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/notify_morning.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

# ── 2. Evening reminder — 8:00 PM daily ───────────────────────────────────────
cat > "$PLIST_DIR/${EVENING_LABEL}.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${EVENING_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON}</string>
        <string>${SCRIPT}</string>
        <string>notify</string>
        <string>evening</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>   <integer>20</integer>
        <key>Minute</key> <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/notify_evening.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/notify_evening.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

# ── 3. Weekly review reminder — Sunday 7:00 PM ────────────────────────────────
cat > "$PLIST_DIR/${WEEKLY_LABEL}.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${WEEKLY_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON}</string>
        <string>${SCRIPT}</string>
        <string>notify</string>
        <string>weekly</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key> <integer>0</integer>
        <key>Hour</key>    <integer>19</integer>
        <key>Minute</key>  <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${LOG_DIR}/notify_weekly.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/notify_weekly.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

# ── Load all agents ────────────────────────────────────────────────────────────
for label in $MORNING_LABEL $EVENING_LABEL $WEEKLY_LABEL; do
    launchctl unload "$PLIST_DIR/${label}.plist" 2>/dev/null  # unload first if re-running
    launchctl load   "$PLIST_DIR/${label}.plist"
    if [ $? -eq 0 ]; then
        echo "  ✅ Loaded: $label"
    else
        echo "  ❌ Failed: $label — check $PLIST_DIR/${label}.plist"
    fi
done

# ── 4. Terminal auto-briefing — fires every time you open terminal ─────────────
# Check if already added
if ! grep -q "prep.py.*notify.*terminal" ~/.zshrc 2>/dev/null; then
    echo "" >> ~/.zshrc
    echo "# SDE Prep Tracker — daily briefing on terminal open" >> ~/.zshrc
    echo "${PYTHON} ${SCRIPT} notify terminal 2>/dev/null" >> ~/.zshrc
    echo "  ✅ Terminal briefing added to ~/.zshrc"
else
    echo "  ✅ Terminal briefing already in ~/.zshrc"
fi

# ── 5. Test notification immediately ──────────────────────────────────────────
echo ""
echo "Sending test notification..."
osascript -e 'display notification "Reminders are set up! You will get alerts at 6AM, 8PM, and Sunday 7PM." with title "✅ SDE Prep Tracker Active" sound name "Ping"'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Done! Reminders active:"
echo ""
echo "  ☀️  6:00 AM daily       — Morning LeetCode reminder + streak alert"
echo "  📚  8:00 PM daily       — Evening study + log reminder"
echo "  📊  Sunday 7:00 PM      — Weekly review reminder"
echo "  💻  Every terminal open — Quick daily briefing (1 line)"
echo ""
echo "To remove all reminders:  bash setup_reminders.sh --remove"
echo "To test right now:        prep notify morning"
echo ""
