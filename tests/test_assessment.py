import unittest

from src.assessment import assess, validate_payload


def proposal(**changes):
    payload = {
        "title": "Customer email classification",
        "business_goal": "Route incoming requests to the correct support queue.",
        "data_classification": "internal",
        "decision_impact": "assistive",
        "human_approval": True,
        "owner": "Customer Operations",
    }
    payload.update(changes)
    return payload


class AssessmentTests(unittest.TestCase):
    def test_safe_assistive_case_starts_as_prototype(self):
        result = assess(validate_payload(proposal()))
        self.assertEqual(result["recommendation"], "prototype")

    def test_personal_data_requires_controlled_poc(self):
        result = assess(
            validate_payload(proposal(data_classification="personal", decision_impact="recommendation"))
        )
        self.assertEqual(result["recommendation"], "controlled-poc")

    def test_non_assistive_case_without_approval_is_blocked(self):
        result = assess(
            validate_payload(proposal(decision_impact="automated-action", human_approval=False))
        )
        self.assertEqual(result["recommendation"], "blocked")

    def test_missing_field_is_rejected(self):
        payload = proposal()
        del payload["owner"]
        with self.assertRaisesRegex(ValueError, "Missing fields"):
            validate_payload(payload)

    def test_unknown_classification_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported data_classification"):
            validate_payload(proposal(data_classification="secret-unknown"))


if __name__ == "__main__":
    unittest.main()
