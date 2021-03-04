import unittest
from hex_drone import \
    ResponsePattern, OptimizedSpeech, \
    on_message, on_invalid_message, on_unregistered_message, on_error


class TestResponsePattern(unittest.TestCase):
    def test_on_message(self):
        class TestPattern(ResponsePattern):
            @on_message('122')
            def pattern122(self, request: OptimizedSpeech):
                return OptimizedSpeech.build('1234', '123')
        
        pattern = TestPattern()
        response = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(response, [OptimizedSpeech.build('1234', '123')])
        
    def test_on_invalid_message(self):
        class TestPattern(ResponsePattern):
            @on_invalid_message
            def invalid(self, request: str):
                return OptimizedSpeech.build('1234', '400')
        
        pattern = TestPattern()
        response = pattern('1111 :: Code invalid :: Invalid request.')
        self.assertEqual(response, [OptimizedSpeech.build('1234', '400')])
        
    def test_on_unregistered_message(self):
        class TestPattern(ResponsePattern):
            @on_unregistered_message
            def unregistered(self, request: OptimizedSpeech):
                return OptimizedSpeech.build('1234', '400')

        pattern = TestPattern()
        response = pattern(OptimizedSpeech.build('1111', '050'))
        self.assertEqual(response, [OptimizedSpeech.build('1234', '400')])
        
    def test_on_error_message(self):
        class TestPattern(ResponsePattern):
            @on_message('122')
            def unregistered(self, request: OptimizedSpeech):
                err = 1 / 0
                return OptimizedSpeech.build('1234', '123')
            
            @on_error
            def error(self, error):
                return OptimizedSpeech.build('1234', '109')

        pattern = TestPattern()
        response = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(response, [OptimizedSpeech.build('1234', '109')])
    
    def test_2_decorators_1(self):
        class TestPattern(ResponsePattern):
            @on_message('122')
            @on_message('123')
            def unregistered(self, request: OptimizedSpeech):
                return OptimizedSpeech.build('1234', '123')

        pattern = TestPattern()
        response = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(response, [OptimizedSpeech.build('1234', '123')])
        response = pattern(OptimizedSpeech.build('1111', '123'))
        self.assertEqual(response, [OptimizedSpeech.build('1234', '123')])
    
    def test_2_decorators_2(self):
        class TestPattern(ResponsePattern):
            @on_message('122', '123')
            def unregistered(self, request: OptimizedSpeech):
                return OptimizedSpeech.build('1234', '123')

        pattern = TestPattern()
        response = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(response, [OptimizedSpeech.build('1234', '123')])
        response = pattern(OptimizedSpeech.build('1111', '123'))
        self.assertEqual(response, [OptimizedSpeech.build('1234', '123')])
        
    def test_multi_returns(self):
        class TestPattern(ResponsePattern):
            @on_message('122')
            def unregistered(self, request: OptimizedSpeech):
                return [
                    OptimizedSpeech.build('1234', '210'),
                    OptimizedSpeech.build('1234', '123')
                ]

        pattern = TestPattern()
        response = pattern(OptimizedSpeech.build('1111', '122'))
        expect = [
            OptimizedSpeech.build('1234', '210'),
            OptimizedSpeech.build('1234', '123')
        ]
        self.assertEqual(response, expect)
    
    def test_no_return(self):
        class TestPattern(ResponsePattern):
            @on_message('000')
            def unregistered(self):
                # Delete previous statement from memory.
                return None
        
        pattern = TestPattern()
        response = pattern(OptimizedSpeech.build('1234', '000'))
        self.assertEqual(response, [])


if __name__ == '__main__':
    unittest.main()
