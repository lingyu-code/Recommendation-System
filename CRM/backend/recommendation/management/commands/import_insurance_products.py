import csv
from django.core.management.base import BaseCommand
from recommendation.models import InsuranceProduct


class Command(BaseCommand):
    help = "Import insurance products from CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="insurance_products.csv",
            help="Path to the CSV file (default: insurance_products.csv)"
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        self.stdout.write(self.style.NOTICE(f"Importing from {file_path}..."))

        objs = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 注意：CSV 表头和模型字段的映射
                objs.append(InsuranceProduct(
                    category=row["险种大类"],
                    subcategory=row["具体险种"],
                    name=row["代表产品（公司）"],
                    coverage_summary=row["保障内容简述"],
                    payout_limit=row["赔付/保额上限"],
                    deductible_and_ratio=row["免赔&给付比例"],
                    base_premium=row["基准保费（18岁/个人/年，除非注明）"],
                    tags=row["关键词标签"],
                ))

        InsuranceProduct.objects.bulk_create(objs, batch_size=500)
        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(objs)} insurance products"))
