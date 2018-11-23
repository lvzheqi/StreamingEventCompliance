import unittest
from streaming_event_compliance.objects.automata import AnonymousSurvey

class TestAnonymousSurvey(unittest.TestCase):
    # 针对AnonymousSurvey类的测试(testClass类)"""
    def setUp(self):
        """创建一个测试对象和测试结果"""
        question = "What language did you first learn to speak?"
        self.my_survey = AnonymousSurvey(question)
        self.responses = ['English', 'Spanish', 'Mandarin']


    def test_store_single_response(self):
        """测试单个答案会被妥善保存"""
        self.my_survey.store_response(self.responses[0])
        self.assertIn(self.responses[0], self.my_survey.responses)

    def test_store_three_response(self):
        """测试三个答案会被妥善保存"""
        for response in self.responses:
            self.my_survey.store_response(response)
        for response in self.responses:
            self.assertIn(response, self.my_survey.responses)

suite = unittest.TestLoader().loadTestsFromTestCase(TestAnonymousSurvey)
unittest.TextTestRunner(verbosity=2).run(suite)

