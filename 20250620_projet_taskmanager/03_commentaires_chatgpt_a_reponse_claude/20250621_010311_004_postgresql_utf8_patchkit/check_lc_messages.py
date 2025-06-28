# check_lc_messages.py
import psycopg2
import logging

logger = logging.getLogger(__name__)

def warn_if_bad_locale(conn):
    cur = conn.cursor()
    cur.execute("SHOW lc_messages;")
    locale = cur.fetchone()[0]
    if locale != "C":
        logger.warning(f"⚠️ PostgreSQL locale 'lc_messages' = {locale} ≠ 'C' → risque UnicodeDecodeError.")




