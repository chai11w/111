import csv
import unittest
from pathlib import Path

from src.roi_filter import classify_roi, load_and_classify_ads


class RoiFilterTest(unittest.TestCase):
    def test_classify_roi_boundaries(self):
        self.assertEqual(classify_roi(1.19, 1.2, 3.0)[0], "低效广告")
        self.assertEqual(classify_roi(3.01, 1.2, 3.0)[0], "优质广告")
        self.assertIsNone(classify_roi(1.2, 1.2, 3.0))
        self.assertIsNone(classify_roi(3.0, 1.2, 3.0))

    def test_load_and_classify_sample_data(self):
        classified_ads = load_and_classify_ads(Path("data/ad_data_sample.csv"))

        low_ads = [ad for ad in classified_ads if ad.alert_type == "低效广告"]
        high_ads = [ad for ad in classified_ads if ad.alert_type == "优质广告"]

        self.assertEqual(len(classified_ads), 8)
        self.assertEqual(len(low_ads), 4)
        self.assertEqual(len(high_ads), 4)
        self.assertEqual({ad.row["platform"] for ad in classified_ads}, {"Facebook", "Google", "TikTok"})

    def test_sample_data_has_owner_and_category_after_platform(self):
        with Path("data/ad_data_sample.csv").open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            self.assertEqual(reader.fieldnames[:5], ["date", "platform", "owner", "category", "campaign_name"])
            rows = list(reader)

        self.assertEqual({row["owner"] for row in rows}, {"Alice", "Ben", "Cindy"})
        self.assertEqual({row["category"] for row in rows}, {"Beauty", "Electronics", "Home"})


if __name__ == "__main__":
    unittest.main()
