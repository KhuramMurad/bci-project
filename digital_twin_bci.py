import random

class EEGData:
    def __init__(self, channels=8):
        # Generate some mock EEG data (e.g., random values between -50.0 and 50.0 microvolts)
        self.eeg = [random.uniform(-50.0, 50.0) for _ in range(channels)]

class DigitalTwinBCI:
    def __init__(self):
        pass

    def generate_realistic_eeg(self):
        # Return a mock EEG data object with 8 channels
        return EEGData(channels=8)
