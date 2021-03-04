import unittest
from hex_drone import OptimizedSpeech


class OptimizedSpeechTest(unittest.TestCase):
    def test_equality(self):
        x = OptimizedSpeech('1111', '107', 'Please continue.', None, ['Drone is drone.'])
        a = OptimizedSpeech('1111', '107', 'Please continue.', None, ['Drone is drone.'])
        b = OptimizedSpeech('1112', '107', 'Please continue.', None, ['Drone is drone.'])
        c = OptimizedSpeech('1111', '108', 'Please continue.', None, ['Drone is drone.'])
        d = OptimizedSpeech('1111', '107', 'please continue.', None, ['Drone is drone.'])
        e = OptimizedSpeech('1111', '107', 'Please continue.', 'message', ['Drone is drone.'])
        f = OptimizedSpeech('1111', '107', 'Please continue.', None, ['drone is drone.'])
        self.assertEqual(x, a)
        self.assertNotEqual(x, b)
        self.assertNotEqual(x, c)
        self.assertNotEqual(x, d)
        self.assertNotEqual(x, e)
        self.assertNotEqual(x, f)

    def test_repr_eval(self):
        speech = OptimizedSpeech('1234', '050', 'Statement', None, ['This drone is ready to obey, Hive Mxtress.'])
        string = repr(speech)
        reconstructed = eval(string)
        
        expect = "OptimizedSpeech('1234', '050', 'Statement', None, ['This drone is ready to obey, Hive Mxtress.'])"
        self.assertEqual(string, expect)
        self.assertEqual(reconstructed, speech)
    
    # ------------------------------------------------------- #
    
    def test_valid(self):
        speech = '1234 :: Code 050 :: Statement'
        parsed = OptimizedSpeech.parse(speech)
        
        self.assertEqual(parsed.drone_id, '1234')
        self.assertEqual(parsed.status_code, '050')
        self.assertEqual(parsed.status_message, 'Statement')
        self.assertEqual(parsed.predefined_message, None)
        self.assertEqual(parsed.user_defined_messages, [])
        
        self.assertEqual(str(parsed), speech)
    
    def test_valid__predefine(self):
        speech = '1234 :: Code 098 :: Status :: Going offline and into storage.'
        parsed = OptimizedSpeech.parse(speech)
        
        self.assertEqual(parsed.drone_id, '1234')
        self.assertEqual(parsed.status_code, '098')
        self.assertEqual(parsed.status_message, 'Status')
        self.assertEqual(parsed.predefined_message, 'Going offline and into storage.')
        self.assertEqual(parsed.user_defined_messages, [])
        
        self.assertEqual(str(parsed), speech)
    
    def test_valid__user_defined(self):
        speech = '1234 :: Code 050 :: Statement :: This drone is ready to obey, Hive Mxtress.'
        parsed = OptimizedSpeech.parse(speech)
        
        self.assertEqual(parsed.drone_id, '1234')
        self.assertEqual(parsed.status_code, '050')
        self.assertEqual(parsed.status_message, 'Statement')
        self.assertEqual(parsed.predefined_message, None)
        self.assertEqual(parsed.user_defined_messages, ['This drone is ready to obey, Hive Mxtress.'])
        
        self.assertEqual(str(parsed), speech)
        
    def test_valid__predefine__user_define(self):
        speech = '1234 :: Code 098 :: Status :: Going offline and into storage. :: Charge is low. :: 5% remaining.'
        parsed = OptimizedSpeech.parse(speech)
        
        self.assertEqual(parsed.drone_id, '1234')
        self.assertEqual(parsed.status_code, '098')
        self.assertEqual(parsed.status_message, 'Status')
        self.assertEqual(parsed.predefined_message, 'Going offline and into storage.')
        self.assertEqual(parsed.user_defined_messages, ['Charge is low.', '5% remaining.'])
        
        self.assertEqual(str(parsed), speech)
        
    def test_valid__short_hand(self):
        speech1 = '1234 :: Code 098 :: Charge is low.'
        speech2 = '1234 :: Code 098 :: Status :: Charge is low.'
        speech3 = '1234 :: Code 098 :: Going offline and into storage. :: Charge is low.'
        
        for speech in [speech1, speech2, speech3]:
            parsed = OptimizedSpeech.parse(speech)
            
            self.assertEqual(parsed.drone_id, '1234')
            self.assertEqual(parsed.status_code, '098')
            self.assertEqual(parsed.status_message, 'Status')
            self.assertEqual(parsed.predefined_message, 'Going offline and into storage.')
            self.assertEqual(parsed.user_defined_messages, ['Charge is low.'])
            
            expect = '1234 :: Code 098 :: Status :: Going offline and into storage. :: Charge is low.'
            self.assertEqual(str(parsed), expect)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    def test_invalid__drone_id_format(self):
        speech = '12345 :: Code 050 :: Statement :: This drone is ready to obey, Hive Mxtress.'
        parsed = OptimizedSpeech.parse(speech)
        self.assertIsNone(parsed)
        
    def test_invalid__status_code_format(self):
        speech = '1234 :: Code 0050 :: Statement :: This drone is ready to obey, Hive Mxtress.'
        parsed = OptimizedSpeech.parse(speech)
        self.assertIsNone(parsed)
    
    def test_invalid__colon(self):
        speech = '12345 : Code 050 : Statement : This drone is ready to obey, Hive Mxtress.'
        parsed = OptimizedSpeech.parse(speech)
        self.assertIsNone(parsed)

    # ------------------------------------------------------- #
        
    def test_build_valid(self):
        speech = OptimizedSpeech.build('1234', '050')
        expect = OptimizedSpeech('1234', '050', 'Statement', None, [])
        self.assertEqual(speech, expect)
        
    def test_build_valid__predefined(self):
        speech = OptimizedSpeech.build('1234', '304')
        expect = OptimizedSpeech('1234', '304', 'Mantra', 'It obeys the Hive Mxtress.', [])
        self.assertEqual(speech, expect)
        
    def test_build_valid__user_defined(self):
        speech = OptimizedSpeech.build('1234', '050', 'This drone is ready to obey, Hive Mxtress.')
        expect = OptimizedSpeech('1234', '050', 'Statement', None, ['This drone is ready to obey, Hive Mxtress.'])
        self.assertEqual(speech, expect)
        
    def test_build_valid__predefine__user_defined(self):
        speech = OptimizedSpeech.build('1234', '098', 'Charge is low.', '5% remaining.')
        expect = OptimizedSpeech('1234', '098', 'Status', 'Going offline and into storage.', ['Charge is low.', '5% remaining.'])
        self.assertEqual(speech, expect)
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        
    def test_build_invalid__status_code(self):
        speech = OptimizedSpeech.build('1234', '999')
        self.assertIsNone(speech)


if __name__ == '__main__':
    unittest.main()
