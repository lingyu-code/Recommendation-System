import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from recommendation.models import StockInfo


class Command(BaseCommand):
    help = "Import stock info from CSV into StockInfo model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="stock_info.csv",
            help="Path to the CSV file (default: stock_info.csv)"
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        self.stdout.write(self.style.NOTICE(f"Importing from {file_path}..."))

        objs = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    list_date = datetime.strptime(row["list_date"], "%Y%m%d").date()
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"❌ Invalid date format: {row['list_date']}"))
                    continue

                objs.append(StockInfo(
                    ts_code=row["ts_code"],
                    symbol=row["symbol"],
                    name=row["name"],
                    area=row["area"],
                    industry=row["industry"],
                    list_date=list_date,
                ))

        # 批量插入，避免重复 (unique=True on ts_code)
        StockInfo.objects.bulk_create(
            objs,
            batch_size=500,
            ignore_conflicts=True  # 遇到重复 ts_code 时跳过
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(objs)} stock info records"))
