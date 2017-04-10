import unittest
from unittest import mock
from gather import commands


class TestCommands(unittest.TestCase):
    def test_help(self):
        self.assertEqual(
            ['Hello!'],
            commands.strip_help(mock.Mock(actions={
                'friendly': ['testregex', mock.Mock(__doc__='Hello!')]
            }))
        )

    def test_format_team(self):
        self.assertEqual(
            """TestPlayer
TestPlayer2
TestPlayer3""",
            commands.format_team(['TestPlayer', 'TestPlayer2', 'TestPlayer3'])
        )


if __name__ == '__main__':
    unittest.main()
