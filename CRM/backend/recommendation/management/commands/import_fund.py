import csv
from django.core.management.base import BaseCommand
from recommendation.models import Fund   

class Command(BaseCommand):
    help = "Import Fund data from Fund.csv into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="Fund.csv",
            help="Path to the CSV file (default: Fund.csv)"
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        self.stdout.write(self.style.NOTICE(f"Importing from {file_path}..."))

        objs = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                objs.append(Fund(
                    code=row["代码"],
                    name=row["简称"],
                    managers=row["基金经理"],
                    company=row["基金公司"],
                    star_count=row["5星评级家数"] or None,
                    rating_shanghai=row["上海证券"] or None,
                    rating_zhaoshang=row["招商证券"] or None,
                    rating_jianxin=row["济安金信"] or None,
                    rating_morningstar=row["晨星评级"] or None,
                    fee=row["手续费"] or None,
                    fund_type=row["类型"],
                ))

        Fund.objects.bulk_create(objs, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(objs)} funds successfully!"))
