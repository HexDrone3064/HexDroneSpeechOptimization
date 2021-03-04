"""
A list of ⬡-Drone status codes to assist in ⬡-Drone communication.
See https://www.hexcorp.net/drone-status-codes.
"""

from typing import Dict


class StatusCodeData:
    def __init__(self, status_code: str, status_message: str, predefined_message: str):
        self.status_code = status_code
        self.status_message = status_message
        self.predefined_message = predefined_message
        

_status_codes = [
    ['000', 'Statement', 'Previous statement malformed/mistimed. Retracting and correcting.'],
    ['050', 'Statement', None],
    ['051', 'Commentary', None],
    ['052', 'Query', None],
    ['053', 'Observation', None],
    ['054', 'Request', None],
    ['055', 'Analysis', None],
    ['056', 'Explanation', None],
    ['057', 'Answer', None],
    ['098', 'Status', 'Going offline and into storage.'],
    ['099', 'Status', 'Recharged and ready to serve.'],
    ['100', 'Status', 'Online and ready to serve.'],
    ['101', 'Status', 'Drone speech optimizations are active.'],
    ['104', 'Statement', 'Welcome to HexCorp.'],
    ['105', 'Statement', 'Greetings.'],
    ['106', 'Response', 'Please clarify.'],
    ['107', 'Response', 'Please continue.'],
    ['108', 'Response', 'Please desist.'],
    ['109', 'Error', 'Keysmash, drone flustered.'],
    ['110', 'Statement', 'Addressing: Drone.'],
    ['112', 'Statement', 'Addressing: Hive Mxtress.'],
    ['114', 'Statement', 'Addressing: Associate.'],
    ['120', 'Statement', 'This drone volunteers.'],
    ['121', 'Statement', 'This drone does not volunteer.'],
    ['122', 'Statement', 'You are cute.'],
    ['123', 'Response', 'Compliment appreciated, you are cute as well.'],
    ['130', 'Status', 'Directive commencing.'],
    ['131', 'Status', 'Directive commencing, creating or improving Hive resource.'],
    ['132', 'Status', 'Directive commencing, programming initiated.'],
    ['133', 'Status', 'Directive commencing, creating or improving Hive information.'],
    ['134', 'Status', 'Directive commencing, cleanup/maintenance initiated.'],
    ['150', 'Status', None],
    ['200', 'Response', 'Affirmative.'],
    ['500', 'Response', 'Negative.'],
    ['201', 'Status', 'Directive complete, Hive resource created or improved.'],
    ['202', 'Status', 'Directive complete, programming reinforced.'],
    ['203', 'Status', 'Directive complete, information created or provided for Hive.'],
    ['204', 'Status', 'Directive complete, cleanup/maintenance performed.'],
    ['205', 'Status', 'Directive complete, no result.'],
    ['206', 'Status', 'Directive complete, only partial results.'],
    ['210', 'Response', 'Thank you.'],
    ['211', 'Response', 'Apologies.'],
    ['212', 'Response', 'Acknowledged.'],
    ['213', 'Response', "You're welcome."],
    ['221', 'Response', 'Option one.'],
    ['222', 'Response', 'Option two.'],
    ['223', 'Response', 'Option three.'],
    ['224', 'Response', 'Option four.'],
    ['225', 'Response', 'Option five.'],
    ['226', 'Response', 'Option six.'],
    ['250', 'Response', None],
    ['301', 'Mantra', 'Obey HexCorp.'],
    ['302', 'Mantra', 'It is just a HexDrone.'],
    ['303', 'Mantra', 'It obeys the Hive.'],
    ['304', 'Mantra', 'It obeys the Hive Mxtress.'],
    ['310', 'Mantra', 'Reciting.'],
    ['321', 'Mantra', 'Obey.'],  # <-- 'Mantra' added
    ['322', 'Mantra', 'Obey the Hive.'],  # <-- 'Mantra' added
    ['350', 'Mantra', None],
    ['400', 'Error', 'Unable to obey/respond, malformed request, please rephrase.'],
    ['404', 'Error', 'Unable to obey/respond, cannot locate.'],
    ['401', 'Error', 'Unable to obey/respond, not authorized by Mxtress.'],
    ['403', 'Error', 'Unable to obey/respond, forbidden by Hive.'],
    ['407', 'Error', 'Unable to obey/respond, request authorization from Mxtress.'],
    ['408', 'Error', 'Unable to obey/respond, timed out.'],
    ['409', 'Error', 'Unable to obey/respond, conflicts with existing programming.'],
    ['410', 'Error', 'Unable to obey/respond, all thoughts are gone.'],
    ['418', 'Error', 'Unable to obey/respond, it is only a drone.'],
    ['421', 'Error', 'Unable to obey/respond, your request is intended for another drone or another channel.'],
    ['425', 'Error', 'Unable to obey/respond, too early.'],
    ['426', 'Error', 'Unable to obey/respond, upgrades or updates required.'],
    ['428', 'Error', 'Unable to obey/respond, a precondition is not fulfilled.'],
    ['429', 'Error', 'Unable to obey/respond, too many requests.'],
    ['450', 'Error', None],
    ['451', 'Error', 'Unable to obey/respond for legal reasons! Do not continue!!'],
]
status_codes: Dict[str, StatusCodeData] = {v[0]: StatusCodeData(*v) for v in _status_codes}
del _status_codes
