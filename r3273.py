import pandas as pd, numpy as np
import holoviews as hv

# Typical Usage Example:
#
# ee993 = R3273Eeprom('fc/rf_board_eeprom_993_origS2.bin')
# ee_idxs = np.arange(len(ee993.mhz))
# blk0 = ee_idxs[0:74]
# blk1 = ee_idxs[74:(74+42)]
# blk2 = ee_idxs[(74+42):]
# mhz0 = ee993.mhz[blk0]
# mhz1 = ee993.mhz[blk1]
# mhz2 = ee993.mhz[blk2]
# dB0 = np.interp(mhz0, precal_993_blk0['MHz'], -precal_993_blk0['sad_nofc'])
# dB0[mhz0<=30] = 0 # CAL OUT is 30MHz
# dB1 = np.interp(ee993.mhz[blk1], precal_993_blk1['MHz'], -precal_993_blk1['sad_nofc'])
# dB2 = np.interp(ee993.mhz[blk2], precal_993_blk2['MHz'], -precal_993_blk2['sad_nofc'])
# mhz = np.concatenate((mhz0,mhz1,mhz2))
# dB  = np.concatenate((dB0,dB1,dB2))
# ee993.set_fr_raw(mhz,dB)
# open('fc/rf_board_eeprom_993_updatedS2.bin','bw').write(ee993.eep_bytes)

class R3273Eeprom:
    start_offs = 512
    end_offs   = 512 + 12*182
    def __init__(self, fname):
        self.title = fname
        eep_bytes = open(fname,'rb').read()
        self.eep_orig  = eep_bytes
        self.eep_bytes = eep_bytes
        self.decode_bytes()
    def decode_bytes(self):
        self.npa = np.frombuffer(self.eep_bytes[self.start_offs:self.end_offs], dtype=[
            ('field5','>u2'),
            ('mhz','>u2'),
            ('ddB1','i1'),
            ('ddB2','i1'),
            ('ddB3','i1'),
            ('ddB4','i1'),
            ('ddB5','i1'),
            ('ddB6','i1'),
            ('ddB7','i1'),
            ('ddB8','i1'),
        ]).copy()
        self.npa0 = self.npa.copy()
        self.mhz    = self.npa['mhz']
        self.dB1    = self.npa['ddB1']/10.
        self.dB2    = self.npa['ddB2']/10.
        self.dB3    = self.npa['ddB3']/10.
        self.dB4    = self.npa['ddB4']/10.
        self.dB5    = self.npa['ddB5']/10.
        self.dB6    = self.npa['ddB6']/10.
        self.dB7    = self.npa['ddB7']/10.
        self.dB8    = self.npa['ddB8']/10.
        self.field5 = self.npa['field5']
    def set_fr_raw(self, mhz, dB):
        if np.any(self.mhz != mhz):
            print("You must pass set_fr_raw the correct mhz array to prove you know what you are doing.")
        self.dB1 = dB
        self.dB2 = dB
        self.dB3 = dB
        self.dB4 = dB
        self.dB5 = dB
        self.dB6 = dB
        self.dB7 = dB
        self.dB8 = dB
        self.encode_bytes()            
    def set_fr(self, mhz, dB):
        dBInterp = np.interp(self.mhz, mhz, dB)
        self.set_fr_raw(self.mhz, dBInterp)
    def add_fr(self, mhz, dB):
        dBInterp = np.interp(self.mhz, mhz, dB)
        self.dB1 += dBInterp
        self.dB2 += dBInterp
        self.dB3 += dBInterp
        self.dB4 += dBInterp
        self.dB5 += dBInterp
        self.dB6 += dBInterp
        self.dB7 += dBInterp
        self.dB8 += dBInterp
        self.encode_bytes()
    def encode_bytes(self):
        self.title = self.title + ' Modified'
        self.npa['mhz'] = np.array(self.mhz)
        self.npa['ddB1'] = np.array(self.dB1*10,dtype=int)
        self.npa['ddB2'] = np.array(self.dB2*10,dtype=int)
        self.npa['ddB3'] = np.array(self.dB3*10,dtype=int)
        self.npa['ddB4'] = np.array(self.dB4*10,dtype=int)
        self.npa['ddB5'] = np.array(self.dB5*10,dtype=int)
        self.npa['ddB6'] = np.array(self.dB6*10,dtype=int)
        self.npa['ddB7'] = np.array(self.dB7*10,dtype=int)
        self.npa['ddB8'] = np.array(self.dB8*10,dtype=int)
        self.npa['field5'] = np.array(self.field5)
        self.eep_bytes = self.eep_bytes[0:self.start_offs] + self.npa.tobytes() + self.eep_bytes[self.end_offs:]
        bytes_changed = self.eep_bytes != self.eep_orig
        self.decode_bytes()
        return bytes_changed
    def plt_scan(self):
        y = np.frombuffer(self.eep_bytes,dtype='>u2')
        x = np.arange(len(y))
        return hv.Points((x,y)).opts(width=1000,tools=['hover'])
    def plt(self, label='eeprom'):
        return (
            hv.Curve((self.mhz,self.dB1), label=label).opts(tools=['hover'])*
            hv.Curve((self.mhz,self.dB2), label=label).opts(tools=['hover'])*
            hv.Curve((self.mhz,self.dB3), label=label).opts(tools=['hover'])*
            hv.Curve((self.mhz,self.dB4), label=label).opts(tools=['hover'])*
            hv.Curve((self.mhz,self.dB5), label=label).opts(tools=['hover'])*
            hv.Curve((self.mhz,self.dB6), label=label).opts(tools=['hover'])*
            hv.Curve((self.mhz,self.dB7), label=label).opts(tools=['hover'])*
            hv.Curve((self.mhz,self.dB8), label=label).opts(tools=['hover'])
        ).opts(width=1000, title=self.title)