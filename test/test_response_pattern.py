import unittest
from hex_drone import \
    ResponsePattern, OptimizedSpeech, RequestEvent as Ev


class TestResponsePattern(unittest.TestCase):
    def test_on_message(self):
        class TestPattern(ResponsePattern):
            response = OptimizedSpeech.build('1234', '123')
            
            @Ev.ON_MESSAGE('122')
            def pattern122(self, request: OptimizedSpeech):
                return self.response
        
        pattern = TestPattern()
        
        expected = (Ev.ON_MESSAGE, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(expected, actual)
        
    def test_on_invalid_message(self):
        class TestPattern(ResponsePattern):
            response = OptimizedSpeech.build('1234', '400')
            
            @Ev.ON_INVALID
            def invalid(self, request: str):
                return self.response
        
        pattern = TestPattern()
        
        expected = (Ev.ON_INVALID, pattern.response)
        actual = pattern('1111 :: Code invalid :: Invalid request.')
        self.assertEqual(expected, actual)
        
    def test_on_unregistered_message(self):
        class TestPattern(ResponsePattern):
            response = OptimizedSpeech.build('1234', '400')

            @Ev.ON_UNREGISTERED
            def unregistered(self, request: OptimizedSpeech):
                return self.response

        pattern = TestPattern()
        
        expected = (Ev.ON_UNREGISTERED, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '050'))
        self.assertEqual(expected, actual)
        
    def test_on_error_message(self):
        class TestPattern(ResponsePattern):
            response = OptimizedSpeech.build('1234', '109')
            
            @Ev.ON_MESSAGE('122')
            def pattern122(self, request: OptimizedSpeech):
                err = 1 / 0
                return OptimizedSpeech.build('1234', '123')
            
            @Ev.ON_ERROR
            def error(self, error):
                return self.response

        pattern = TestPattern()
        
        expected = (Ev.ON_ERROR, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(expected, actual)
    
    def test_2_decorators_1(self):
        class TestPattern(ResponsePattern):
            response = OptimizedSpeech.build('1234', '123')
            
            @Ev.ON_MESSAGE('122')
            @Ev.ON_MESSAGE('123')
            def patterns(self, request: OptimizedSpeech):
                return self.response

        pattern = TestPattern()
        
        expected = (Ev.ON_MESSAGE, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(expected, actual)
        
        expected = (Ev.ON_MESSAGE, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '123'))
        self.assertEqual(actual, expected)
    
    def test_2_decorators_2(self):
        class TestPattern(ResponsePattern):
            response = OptimizedSpeech.build('1234', '123')
            
            @Ev.ON_MESSAGE('122', '123')
            def patterns(self, request: OptimizedSpeech):
                return self.response

        pattern = TestPattern()
        
        expected = (Ev.ON_MESSAGE, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(expected, actual)

        expected = (Ev.ON_MESSAGE, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '123'))
        self.assertEqual(expected, actual)
        
    def test_multi_returns(self):
        class TestPattern(ResponsePattern):
            response = [
                OptimizedSpeech.build('1234', '210'),
                OptimizedSpeech.build('1234', '123')
            ]
            
            @Ev.ON_MESSAGE('122')
            def pattern122(self, request: OptimizedSpeech):
                return self.response

        pattern = TestPattern()
        
        expected = (Ev.ON_MESSAGE, pattern.response)
        actual = pattern(OptimizedSpeech.build('1111', '122'))
        self.assertEqual(expected, actual)
    
    def test_no_return(self):
        class TestPattern(ResponsePattern):
            response = None
            
            @Ev.ON_MESSAGE('000')
            def pattern000(self, request: OptimizedSpeech):
                return self.response
        
        pattern = TestPattern()
        
        expected = (Ev.ON_MESSAGE, pattern.response)
        actual = pattern(OptimizedSpeech.build('1234', '000'))
        self.assertEqual(expected, actual)
        
    def test_call_with_args(self):
        class TestPattern(ResponsePattern):
            @Ev.ON_MESSAGE('050')
            def pattern050(self, request: OptimizedSpeech, now: str):
                if 'error' in request.user_defined_messages:
                    raise ValueError()
                return OptimizedSpeech.build('1234', '050', now)
            
            @Ev.ON_UNREGISTERED
            def unregistered(self, request: OptimizedSpeech, now: str):
                return OptimizedSpeech.build('1234', '400', now)
            
            @Ev.ON_ERROR
            def error(self, error: BaseException, now: str):
                return OptimizedSpeech.build('1234', '109', now)
        
        pattern = TestPattern()
        from datetime import datetime
        
        now = datetime.now().strftime('%H:%M:%S')
        request = OptimizedSpeech.build('1111', '050')
        expected = (Ev.ON_MESSAGE, OptimizedSpeech.build('1234', '050', now))
        actual = pattern(request, now=now)
        self.assertEqual(expected, actual)
        
        now = datetime.now().strftime('%H:%M:%S')
        request = OptimizedSpeech.build('1111', '050', 'error')
        expected = (Ev.ON_ERROR, OptimizedSpeech.build('1234', '109', now))
        actual = pattern(request, now=now)
        self.assertEqual(expected, actual)
        
        now = datetime.now().strftime('%H:%M:%S')
        request = OptimizedSpeech.build('1111', '105', 'error')
        expected = (Ev.ON_UNREGISTERED, OptimizedSpeech.build('1234', '400', now))
        actual = pattern(request, now=now)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
