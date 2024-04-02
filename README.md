# Advantest R3273 Calibration

This is some code I wrote to calibrate my pair of Advantest R3273 spectrum analyzers. Hopefully other R3273 owners find it helpful as well!

<img src="r3273-714.jpg" width="400">
<img src="r3273-993.jpg" width="400">


# EEPROM

The first step is to obtain read/write capability in the metrology EEPROM. This is stored on a small chip on the interior-facing side of the metrology deck, and I updated it the hard way, by taking measurements, removing the deck, programming the chip, replacing it, and verifying that (thankfully) the act of replacing the deck did not meaningfully degrade the calibration. When connectors with metal mating surfaces are used with proper torque wrenches, it appears that they are somewhat repeatable after all.

That said, if I were doing this again I would pay attention to the recent discoveries of GPIB $R/$W commands on the Advantest mailing list. Using these is likely to be easier and to produce fewer sources of assembly/disassembly variation.

<img src="rfdeck_left.jpg" width="400">
<img src="rfdeck_center_EEPROM.jpg" width="400">

# Files

**r3273.py:** Interprets and modifies binary EEPROM blobs

**r3273_freqcorr.ipynb:** Sweeps SG, PM to gather cal info for SA.

**step_atten_measurements:** S parameters of working step attenuator

**fc:** EEPROM images
