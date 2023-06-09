# Copyright 2020 Bateared Collie
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import unittest


class Test1(unittest.TestCase):
    
    def testUTCDateTime(self):
        '''
        Simple test
        '''
    
        print("\n******************\ntestUTCDateTime\n******************\n")
    
        from obsln import UTCDateTime
    
        uu=UTCDateTime()
        print("uu=",uu)
    
        uu=UTCDateTime(0)
        #print("uu=",uu)
        self.assertEqual(uu.__str__(), "1970-01-01T00:00:00.000000Z", "Test fail")
    
        uu=UTCDateTime(1240561632)
        #print("uu=",uu)
        self.assertEqual(uu.__str__(), "2009-04-24T08:27:12.000000Z", "Test fail")
    
        uu += 1
        #print("uu=",uu)
        self.assertEqual(uu.__str__(), "2009-04-24T08:27:13.000000Z", "Test fail")
    
        uu=UTCDateTime(1240561632.5)
        #print("uu=",uu)
        self.assertEqual(uu.__str__(), "2009-04-24T08:27:12.500000Z", "Test fail")
    
        uu=UTCDateTime("2009-12-31T12:23:34.5")
        #print("uu=",uu)
        self.assertEqual(uu.__str__(), "2009-12-31T12:23:34.500000Z", "Test fail")
    
    def testTrace(self):
    
        print("\n******************\ntestTrace\n******************\n")
    
        #from obsln.core.trace import Stats
        from obsln import Trace
    
        import numpy as np
        tt = np.linspace(0,2,501)
        ff = np.sin(2*np.pi*40*tt)
    
        trc = Trace(data=ff,header={"sampling_rate":250})
        print("trc stats:\n",trc.stats)
        print("\nTrace:\n",trc)
        self.assertEqual(trc.__str__(),
                         "... | 1970-01-01T00:00:00.000000Z - 1970-01-01T00:00:02.000000Z | 250.0 Hz, 501 samples"
                         ,
                         "Test fail")
    
    def testStream(self):
    
        print("\n******************\ntestStream\n******************\n")
    
        from obsln import Stream
        from obsln import Trace
        import numpy as np
    
        st = Stream()
        for ii in range(0,10):
    
            tt = np.linspace(0,2,501)
            ff = np.sin(2*np.pi*40*tt)*(ii+1)
            trc = Trace(data=ff,header={"sampling_rate":250,"station":"stn"+str(ii)})
    
            st.append(trc)
    
        # Print
        print(st)
    
        # itterate
        print("\nTraces:\n")
        for tr in st: print(tr)
    
        print("\nGaps:\n")
        st.print_gaps()
    
    def testSEGY(self):
    
        print("\n******************\ntestSEGY\n******************\n")
    
        # Make some data
        from obsln import Stream
        from obsln import Trace
        import numpy as np
    
        st = Stream()
        for ii in range(0,10):
            tt = np.linspace(0,2,501)
            ff = np.sin(2*np.pi*40*tt,dtype=np.float32)*(ii+1)
            trc = Trace(data=ff,header={"sampling_rate":250,"station":"stn"+str(ii)})
            st.append(trc)
    
        # Write as SEGY
        from obsln.io.segy.core import _write_segy
        _write_segy(st,"test.sgy")
    
        # Read back in full file - standard read function
        print("\n*******\nRead in stream")
        from obsln import read
        rst = read("test.sgy")
    
        # Use the generic writer
        rst.write("test2.segy")
    
        # Read back in headers
        from obsln.io.segy.segy import iread_segy
        for tr in iread_segy("test2.segy"):
            print(tr,np.min(tr.data),np.max(tr.data))
    
        # Reading to internla SEGY object
        from obsln.io.segy.segy import _read_segy
        segy = _read_segy("test.sgy")
        print("segy=",segy)
    
    def testSU(self):
    
        print("\n******************\ntestSU\n******************\n")
    
        # Make some data
        from obsln import Stream
        from obsln import Trace
        import numpy as np
    
        st = Stream()
        for ii in range(0,10):
            tt = np.linspace(0,2,501)
            ff = np.sin(2*np.pi*40*tt,dtype=np.float32)*(ii+1)
            trc = Trace(data=ff,header={"sampling_rate":250,"station":"stn"+str(ii)})
            st.append(trc)
    
        # Write as SU
        st.write("test.su")
    
        from obsln import read
        rst = read("test.su")
        for tr in rst: print(tr)

# SEG2 writing is not supported so cannot test this..
#     def testSEG2(self):
#          
#         print("\n******************\ntestSEG2\n******************\n")
#          
#         # Make some data
#         from obsln import Stream
#         from obsln import Trace
#         import numpy as np
#          
#         st = Stream()
#         for ii in range(0,10):
#             tt = np.linspace(0,2,501)
#             ff = np.sin(2*np.pi*40*tt,dtype=np.float32)*(ii+1)
#             trc = Trace(data=ff,header={"sampling_rate":250,"station":"stn"+str(ii)})
#             st.append(trc)
#  
#         # Write as SU
#         st.write("test.seg",format="SEG2")
#  
# #         from obsln import read
# #         rst = read("test.su")
# #         for tr in rst: print(tr)
    
if __name__ == "__main__":
    
    unittest.main()