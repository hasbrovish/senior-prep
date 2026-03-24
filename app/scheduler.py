"""
Background scheduler — runs intel scraping + trend analysis automatically.
Uses APScheduler (in-process, no Redis/Celery needed for single-user app).
"""

import sys, logging
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    HAS_SCHEDULER = True
except ImportError:
    HAS_SCHEDULER = False

_scheduler = None
log = logging.getLogger("prepforge.scheduler")


def job_scrape_all():
    """Daily: scrape all interview experience sources."""
    log.info("⏰ Scheduled scrape starting...")
    try:
        from intel.scraper import run_scraper
        stats = run_scraper(verbose=False)
        total = sum(s.get("inserted", 0) for s in stats.values())
        log.info(f"  Scrape done: {total} new experiences added")
    except Exception as e:
        log.error(f"  Scrape failed: {e}")


def job_sync_leetcode():
    """Daily: sync LeetCode stats."""
    log.info("⏰ LeetCode sync starting...")
    try:
        import json, urllib.request
        from datetime import date

        prog_file = BASE / "logs" / "progress.json"
        try:
            p = json.loads(prog_file.read_text())
        except Exception:
            p = {}

        username = p.get("lc_sync", {}).get("username", "")
        if not username:
            return

        # LeetCode stats API
        payload = json.dumps({
            "query": """
            query getUserProfile($username: String!) {
              matchedUser(username: $username) {
                submitStatsGlobal {
                  acSubmissionNum {
                    difficulty count submissions
                  }
                }
                languageProblemCount { languageName problemsSolved }
                userCalendar { streak totalActiveDays }
              }
            }""",
            "variables": {"username": username}
        }).encode()
        req = urllib.request.Request(
            "https://leetcode.com/graphql",
            data=payload,
            headers={"Content-Type": "application/json",
                     "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        user = data.get("data", {}).get("matchedUser", {})
        if not user:
            return

        stats = user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
        lang_stats = user.get("languageProblemCount", [])
        cal = user.get("userCalendar", {})

        counts = {s["difficulty"]: s["count"] for s in stats}
        lang_map = {l["languageName"]: l["problemsSolved"] for l in lang_stats}

        total = counts.get("All", 0)
        prev_total = p.get("lc_sync", {}).get("total", 0)

        p.setdefault("lc_sync", {}).update({
            "total": total,
            "easy": counts.get("Easy", 0),
            "medium": counts.get("Medium", 0),
            "hard": counts.get("Hard", 0),
            "streak": cal.get("streak", 0),
            "total_active_days": cal.get("totalActiveDays", 0),
            "java_problems": lang_map.get("Java", 0),
            "cpp_problems": lang_map.get("C++", 0),
            "languages": lang_map,
            "last_sync": str(date.today()),
        })

        if total > prev_total:
            today = str(date.today())
            p.setdefault("daily_logs", {}).setdefault(today, []).append(
                f"[Auto-sync] {total - prev_total} new LC problem(s) (total: {total})"
            )
        prog_file.write_text(json.dumps(p, indent=2, default=str))
        log.info(f"  LC sync done: {total} problems, {lang_map.get('Java',0)} Java")
    except Exception as e:
        log.error(f"  LC sync failed: {e}")


def job_morning_brief():
    """Daily: send morning brief to ntfy.sh."""
    log.info("⏰ Morning brief sending...")
    try:
        from intel.brief import send_morning_brief
        success = send_morning_brief(verbose=False)
        if success:
            log.info("  Morning brief sent via ntfy.sh")
        else:
            log.info("  Morning brief: NTFY_TOPIC not set — skipped push")
    except Exception as e:
        log.error(f"  Morning brief failed: {e}")


def job_weekly_trend_report():
    """Weekly: generate trend report and save to DB."""
    log.info("⏰ Weekly trend analysis starting...")
    try:
        from intel.analyzer import get_trending_topics
        from intel.db import get_conn
        trends = get_trending_topics(days=7)
        log.info(f"  Trend analysis done: {trends.get('total_rounds', 0)} rounds analyzed")
    except Exception as e:
        log.error(f"  Trend analysis failed: {e}")


def start_scheduler():
    global _scheduler
    if not HAS_SCHEDULER:
        log.warning("APScheduler not installed — background jobs disabled")
        return

    _scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    # Daily scrape at 6 AM IST
    _scheduler.add_job(job_scrape_all, CronTrigger(hour=6, minute=0),
                       id="daily_scrape", replace_existing=True)

    # LC sync every 4 hours
    _scheduler.add_job(job_sync_leetcode, CronTrigger(hour="*/4", minute=30),
                       id="lc_sync", replace_existing=True)

    # Daily morning brief at 8 AM IST
    _scheduler.add_job(job_morning_brief, CronTrigger(hour=8, minute=0),
                       id="morning_brief", replace_existing=True)

    # Weekly trend report Sunday 8 AM IST
    _scheduler.add_job(job_weekly_trend_report, CronTrigger(day_of_week="sun", hour=8),
                       id="weekly_trends", replace_existing=True)

    _scheduler.start()
    log.info("Scheduler started: daily scrape 6AM, LC sync every 4h, brief 8AM, weekly trends Sunday")


def stop_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
