import machine
import time

# Initialize the DAC (Digital to Analog Converter) pin (GPIO25 is default)
dac = machine.DAC(machine.Pin(25))

# Open the WAV file (8-bit, mono, 8kHz audio)
with open('Archives/evilmc.wav', 'rb') as f:
    # Skip the WAV header (44 bytes)
    f.read(44)

    # Read the audio data (1 byte at a time)
    print('START')
    while True:
        byte = f.read(1)
        if not byte:
            break
        # Play the audio by writing to the DAC
        dac.write(byte[0])

        # Optional: Add a small delay if needed for the audio playback
        time.sleep(0.0001)
