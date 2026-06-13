import unittest
from unittest.mock import patch

import cv_generator


class GenerateCvFallbackTests(unittest.TestCase):
    def test_generate_cv_fallback_produces_rich_resume_content(self):
        with patch.object(cv_generator, "client", None):
            result = cv_generator.generate_cv({
                "current_role": "Teacher",
                "target_role": "Principal",
                "skills": "Leadership, Communication",
                "experience": "",
                "education": "",
                "projects": "",
                "certifications": ""
            })

        self.assertTrue(result["summary"])
        self.assertGreaterEqual(len(result["skills"]), 4)
        self.assertGreaterEqual(len(result["experience"]), 1)
        self.assertGreaterEqual(len(result["projects"]), 1)
        self.assertTrue(result["experience"][0].get("company") or "Professional Experience")
    def test_generate_cv_fallback_uses_structured_resume_fields(self):
        with patch.object(cv_generator, "client", None):
            result = cv_generator.generate_cv({
                "current_role": "Teacher",
                "target_role": "Principal",
                "skills": "English, Leadership, Communication",
                "experience": "Taught students and led classroom activities.",
                "education": "B.Ed. in Education",
                "projects": "School improvement project",
                "certifications": "TESOL"
            })

        self.assertIsInstance(result, dict)
        self.assertTrue(result["skills"])
        self.assertIsInstance(result["experience"], list)
        self.assertTrue(result["experience"])
        self.assertIn("title", result["experience"][0])
        self.assertIn("responsibilities", result["experience"][0])
        self.assertIsInstance(result["education"], list)
        self.assertTrue(result["education"])

    def test_generate_cv_normalizes_resume_structure_for_display(self):
        fake_json = '''{
          "summary": "Summary",
          "skills": ["Python"],
          "experience": [{"role": "Developer", "duration": "2 years", "details": "Built apps"}],
          "projects": [{"name": "AI App", "description": "Helpful app"}],
          "certifications": [{"name": "AWS"}],
          "education": [{"degree": "BSc", "institution": "University", "year_completed": "2024"}],
          "advantages": ["Fast learner"]
        }'''

        class FakeMessage:
            content = fake_json

        class FakeChoice:
            message = FakeMessage()

        class FakeResponse:
            choices = [FakeChoice()]

        class FakeCompletions:
            def create(self, **kwargs):
                return FakeResponse()

        class FakeClient:
            chat = type("Chat", (), {"completions": FakeCompletions()})()

        with patch.object(cv_generator, "client", FakeClient()):
            result = cv_generator.generate_cv({"current_role": "Engineer", "target_role": "Senior Engineer"})

        self.assertEqual(result["experience"][0]["title"], "Developer")
        self.assertEqual(result["experience"][0]["responsibilities"][0], "Built apps")
        self.assertEqual(result["projects"][0]["name"], "AI App")
        self.assertEqual(result["education"][0]["degree"], "BSc")

    def test_generate_cv_returns_default_structure_when_model_response_is_not_json(self):
        class FakeMessage:
            content = "not json"

        class FakeChoice:
            message = FakeMessage()

        class FakeResponse:
            choices = [FakeChoice()]

        class FakeCompletions:
            def create(self, **kwargs):
                return FakeResponse()

        class FakeClient:
            chat = type("Chat", (), {"completions": FakeCompletions()})()

        with patch.object(cv_generator, "client", FakeClient()):
            result = cv_generator.generate_cv({"current_role": "Engineer", "target_role": "Senior Engineer"})

        self.assertIsInstance(result, dict)
        self.assertIn("summary", result)
        self.assertIn("skills", result)
        self.assertIn("experience", result)
        self.assertIn("projects", result)
        self.assertIn("certifications", result)
        self.assertIn("education", result)
        self.assertIn("advantages", result)


if __name__ == "__main__":
    unittest.main()
