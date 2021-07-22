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




from beep.protocol.maccor import Procedure
import beep.protocol.vizualize_maccor

#Load the procedure for the first test (will change to relative paths, etc. as I move forward)
proc = Procedure.from_file("/Users/alecbills/ResearchProjects/IndustryProjects/Ampaire/maccor/protocols/ampaire_bic_v2_0.000")


thing = proc.convert_to_graph_dict()
proc.vizualize()