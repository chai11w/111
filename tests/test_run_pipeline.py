import unittest
from pathlib import Path

from src.run_pipeline import run_pipeline


class RunPipelineTest(unittest.TestCase):
    def test_run_pipeline_generates_report_and_summary(self):
        output_path = Path("reports/.test_pipeline_report.md")
        result = run_pipeline(Path("data/ad_data_sample.csv"), output_path)
        report = output_path.read_text(encoding="utf-8")

        self.assertEqual(result.total_alerts, 8)
        self.assertEqual(result.low_alerts, 4)
        self.assertEqual(result.high_alerts, 4)
        self.assertEqual(result.output_path, output_path)
        self.assertIn("# ROI 异常广告预警报告", report)
        self.assertIn("异常广告总数：8", report)
        self.assertIn("建议动作：", report)


if __name__ == "__main__":
    unittest.main()
