import time
import argparse
from datetime import datetime
from task_scheduler_cursor import TaskSchedulerCursor

REPORT_PATH = "reports/diagnostic_scheduler_report_{date}.md"


def diagnostic_scheduler(loop: bool = False, interval: int = 10, max_iter: int = 30):
    scheduler = TaskSchedulerCursor()
    iter_count = 0
    print("\n🚦 Diagnostic du Scheduler TaskMaster Cursor")
    print("="*60)
    try:
        while True:
            stats = scheduler.db_manager.get_queue_stats()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] File d'attente : {stats}")
            if not loop or iter_count >= max_iter:
                break
            time.sleep(interval)
            iter_count += 1
    except Exception as e:
        print(f"❌ Erreur critique lors du diagnostic : {e}")
    finally:
        # Générer un rapport
        report_file = REPORT_PATH.format(date=datetime.now().strftime('%Y%m%d_%H%M%S'))
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🚦 Rapport Diagnostic Scheduler\n\n")
            f.write(f"**Date** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Statut file d'attente** : {stats}\n\n")
        print(f"\n📄 Rapport généré : {report_file}")


def main():
    parser = argparse.ArgumentParser(description="Relance et diagnostic du scheduler TaskMaster Cursor")
    parser.add_argument('--loop', action='store_true', help='Boucle de diagnostic (par défaut : une seule itération)')
    parser.add_argument('--interval', type=int, default=10, help='Intervalle entre diagnostics (secondes)')
    parser.add_argument('--max-iter', type=int, default=30, help='Nombre maximal d’itérations en mode boucle')
    args = parser.parse_args()
    diagnostic_scheduler(loop=args.loop, interval=args.interval, max_iter=args.max_iter)

if __name__ == "__main__":
    main() 