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
        
    
    # Trace 
    
    # Stream
    
    # SEGY IO
    
    # SU IO
    
    
if __name__ == "__main__":
    
    unittest.main()