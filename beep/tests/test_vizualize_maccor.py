# Copyright [2020] [Toyota Research Institute]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#TODO: Find a way to test dash

from beep.protocol.maccor import Procedure
import beep.protocol.vizualize_maccor

import unittest 
import os

TEST_DIR = os.path.dirname(__file__)
TEST_FILE_DIR = os.path.join(TEST_DIR, "test_files")

class ProtocolVizualization(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_ampaireProtocol(self):
        proc = Procedure.from_file("/Users/alecbills/ResearchProjects/IndustryProjects/Ampaire/maccor/protocols/ampaire_bic_v2_0.000")
        proc.convert_to_graph_dict()
    
    def test_diagnosticV4(self):
        proc = Procedure.from_file(TEST_FILE_DIR+"/diagnosticV4.000")
        proc.convert_to_graph_dict()
    
    def test_EXP_missing(self):
        proc = Procedure.from_file(TEST_FILE_DIR+"/EXP.000")
        proc.convert_to_graph_dict()

    def test_xTESLA_1(self):
        proc = Procedure.from_file(TEST_FILE_DIR+"/xTESLADIAG_000003_CH68.000")
        proc.convert_to_graph_dict()
            
    def test_xTESLA_2(self):
        proc = Procedure.from_file(TEST_FILE_DIR+"/xTESLADIAG_000004_CH69.000")
        proc.convert_to_graph_dict()
        
if __name__ == "__main__":
    unittest.main()
