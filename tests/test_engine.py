import unittest
from eles_core.engine import Engine

class TestEngine(unittest.TestCase):
    def test_load_config(self):
        engine = Engine('config/settings.yaml')
        self.assertIsNotNone(engine.settings)

if __name__ == '__main__':
    unittest.main()
