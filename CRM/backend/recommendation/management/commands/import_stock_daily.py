import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from recommendation.models import StockDailyData


class Command(BaseCommand):
    help = "Import stock daily data from CSV into StockDailyData model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="stock_daily_data.csv",
            help="Path to the CSV file (default: stock_daily_data.csv)"
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        self.stdout.write(self.style.NOTICE(f"Importing from {file_path}..."))

        objs = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    trade_date = datetime.strptime(row["trade_date"], "%Y%m%d").date()
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"❌ Invalid date format: {row['trade_date']}"))
                    continue

                objs.append(StockDailyData(
                    ts_code=row["ts_code"],
                    trade_date=trade_date,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    pre_close=float(row["pre_close"]),
                    change=float(row["change"]),
                    pct_chg=float(row["pct_chg"]),
                    vol=float(row["vol"]),
                    amount=float(row["amount"]),
                ))

        # 批量插入，避免重复（unique_together）
        StockDailyData.objects.bulk_create(
            objs,
            batch_size=500,
            ignore_conflicts=True  # 遇到重复 (ts_code, trade_date) 时跳过
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(objs)} stock daily records"))
