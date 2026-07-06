import unittest
from pathlib import Path

from src.llm_analyzer import analyze_alert_case, generate_report
from src.roi_filter import load_and_classify_ads


class LlmAnalyzerTest(unittest.TestCase):
    def test_analyze_alert_case_uses_alert_type_without_reclassifying_roi(self):
        alert_case = load_and_classify_ads(Path("data/ad_data_sample.csv"))[0].to_alert_case()
        analysis = analyze_alert_case(alert_case)

        self.assertEqual(analysis.alert_case.alert_type, "低效广告")
        self.assertIn(analysis.priority, {"高", "中", "低"})
        self.assertGreaterEqual(len(analysis.possible_reasons), 1)
        self.assertGreaterEqual(len(analysis.recommended_actions), 1)
        self.assertGreaterEqual(len(analysis.human_check_items), 1)

    def test_generate_report_writes_markdown_file(self):
        output_path = Path("reports/.test_roi_alert_report.md")
        report = generate_report(Path("data/ad_data_sample.csv"), output_path)

        self.assertTrue(output_path.exists())
        self.assertIn("# ROI 异常广告预警报告", report)
        self.assertIn("异常广告总数：8", report)
        self.assertIn("低效广告：4", report)
        self.assertIn("优质广告：4", report)
        self.assertIn("LLM 分析层不判断 ROI 是否达标", report)
        self.assertIn("可能原因：", report)
        self.assertIn("建议动作：", report)
        self.assertIn("需人工确认：", report)


if __name__ == "__main__":
    unittest.main()
