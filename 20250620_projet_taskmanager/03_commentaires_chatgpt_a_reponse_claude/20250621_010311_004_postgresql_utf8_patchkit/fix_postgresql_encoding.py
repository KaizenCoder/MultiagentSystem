#!/usr/bin/env python3
"""Fix UTF-8 PostgreSQL (lc_messages) on Windows"""
import os
import shutil
import time
import re

PG_CONF = r"C:\Program Files\PostgreSQL\17\data\postgresql.conf"
BACKUP = PG_CONF + ".bak"

def patch_lc_messages():
    with open(PG_CONF, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if "lc_messages = 'C'" in content:
        print("✅ lc_messages already set to 'C'")
        return

    shutil.copy2(PG_CONF, BACKUP)
    print(f"📦 Backup saved to {BACKUP}")

    patched = re.sub(r"lc_messages\s*=\s*'.*?'", "lc_messages = 'C'", content)
    if "lc_messages" not in patched:
        patched += "\nlc_messages = 'C'"

    with open(PG_CONF, "w", encoding="utf-8") as f:
        f.write(patched)
    print("🔧 Patched lc_messages = 'C'")

    print("🔄 Restarting PostgreSQL service...")
    os.system("net stop postgresql-x64-17")
    time.sleep(2)
    os.system("net start postgresql-x64-17")
    print("✅ PostgreSQL restarted")

if __name__ == "__main__":
    patch_lc_messages()




