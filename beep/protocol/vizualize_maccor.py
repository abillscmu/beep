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
"""
Module for generating a vizualization of a maccor testing profile
Useful for validation of maccor protocols without requiring loading onto a maccor machine
"""


import pandas as pd
from beep.protocol.maccor import Procedure

import dash
import dash_cytoscape as cyto
import dash_html_components as html

#This function processes all ends of a step
def processNormalStep(procEnds,edgeididx):
    ends = []
    #Enumerate all ends, and add to the list of dicts for graphing
    for (e,thisEnd) in enumerate(procEnds):
        endType = thisEnd['EndType']
        endOper = thisEnd['Oper']
        endValue = thisEnd['Value']
        goto = int(thisEnd['Step'])
        endId = endType+endOper+endValue
        thisEndDict = {
            'condition':endId,
            'goto':goto,
            'edgeidx':str(edgeididx)
        }
        edgeididx=edgeididx+1
        ends.append(thisEndDict)
    return ends,edgeididx

def convert_to_graph_dict(self):
    testSteps = self["MaccorTestProcedure"]["ProcSteps"]["TestStep"]
    edgeididx = -15000 #Maximum number of edges is 15000 (to be improved)
    graphDict = []
    for (s,testStep) in enumerate(testSteps):
        _id = s+1 #Maccor uses base 1 indexing
        thisStep = {'_id':_id}
        stepType = testStep['StepType']
        #Easy Cases: Charge, Discharge, Rest
        if stepType =='Charge':
            stepMode = testStep['StepMode']
            stepValue = testStep['StepValue']
            stepLimits = testStep['Limits']
            procEnds = testStep['Ends']['EndEntry']
            if stepLimits is not None:
                if list(stepLimits.keys())[0] == 'Voltage':
                    #CCCV
                    whatToDo = str(stepValue)+"CC " + str(stepLimits['Voltage'])+"CV"
                    thisStep.update({'step-name':whatToDo})
            else:
                stepMode = testStep['StepMode']
                stepValue = testStep['StepValue']
                whatToDo = "Charge at "+stepMode+" "+stepValue
                thisStep.update({'step-name':whatToDo})
            if type(procEnds) == list:
                ends,edgeididx = processNormalStep(procEnds,edgeididx)
            else:
                endType = procEnds['EndType']
                endOper = procEnds['Oper']
                endValue = procEnds['Value']
                goto = int(procEnds['Step'])
                endId = endType+endOper+endValue
                thisEndDict = {
                    'condition':endId,
                    'goto':goto,
                    'edgeidx':str(edgeididx)
                }
                edgeididx=edgeididx+1
                ends = [thisEndDict,]
            thisStep.update({'ends':ends})
        elif stepType=='Dischrge':
            stepMode = testStep['StepMode']
            stepValue = testStep['StepValue']
            whatToDo = "Discharge at "+stepMode+" "+stepValue
            thisStep.update({'step-name':whatToDo})
            procEnds = testStep['Ends']['EndEntry']
            if type(procEnds) == list:
                ends,edgeididx = processNormalStep(procEnds,edgeididx)
            else:
                endType = procEnds['EndType']
                endOper = procEnds['Oper']
                endValue = procEnds['Value']
                goto = int(procEnds['Step'])
                endId = endType+endOper+endValue
                thisEndDict = {
                    'condition':endId,
                    'goto':goto,
                    'edgeidx':str(edgeididx)
                }
                edgeididx=edgeididx+1
                ends = [thisEndDict,]
            thisStep.update({'ends':ends})
        elif stepType =='Rest':
            thisStep.update({'step-name':"Rest"})
            procEnds = testStep['Ends']['EndEntry']
            ends,edgeididx = processNormalStep(procEnds,edgeididx)
            thisStep.update({'ends':ends})
        elif stepType=='AdvCycle':
            thisStep.update({'step-name':"Advance Cycle"})
            thisStep.update({'ends':[{'condition':"default",'goto':_id+1,'edgeidx':str(edgeididx)}]})
            edgeididx=edgeididx+1
        elif stepType=='Do 1':
            thisStep.update({'step-name':'Do 1'})
            thisStep.update({'ends':[{'condition':"default",'goto':_id+1,'edgeidx':str(edgeididx)}]})
            edgeididx=edgeididx+1
            do1 = _id
        elif stepType=='Do 2':
            thisStep.update({'step-name':'Do 2'})
            thisStep.update({'ends':[{'condition':"default",'goto':_id+1,'edgeidx':str(edgeididx)}]})
            edgeididx=edgeididx+1
            do2 = _id
        elif stepType=='Do 3':
            thisStep.update({'step-name':'Do 3'})
            thisStep.update({'ends':[{'condition':"default",'goto':_id+1,'edgeidx':str(edgeididx)}]})
            edgeididx=edgeididx+1
            do3 = _id
        elif stepType=='Do 4':
            thisStep.update({'step-name':'Do 4'})
            thisStep.update({'ends':[{'condition':"default",'goto':_id+1,'edgeidx':str(edgeididx)}]})
            edgeididx=edgeididx+1
            do4 = _id      
        elif stepType=='Loop 1':
            thisStep.update({'step-name':'Loop 1'})
            ends = [{'condition':"default",'goto':do1,'edgeidx':str(edgeididx)}]
            edgeididx=edgeididx+1
            otherEnds = testStep['Ends']['EndEntry']
            condition = otherEnds['EndType']+otherEnds['Oper']+otherEnds['Value']
            goto = int(otherEnds['Step'])
            ends.append({'condition':condition,'goto':goto,'edgeidx':str(edgeididx)})
            thisStep.update({'ends':ends})
            edgeididx=edgeididx+1
        elif stepType=='Loop 2':
            thisStep.update({'step-name':'Loop 2'})
            ends = [{'condition':"default",'goto':do2,'edgeidx':str(edgeididx)}]
            edgeididx=edgeididx+1
            otherEnds = testStep['Ends']['EndEntry']
            condition = otherEnds['EndType']+otherEnds['Oper']+otherEnds['Value']
            goto = int(otherEnds['Step'])
            ends.append({'condition':condition,'goto':goto,'edgeidx':str(edgeididx)})
            edgeididx=edgeididx+1
            thisStep.update({'ends':ends})
        elif stepType=='Loop 3':
            thisStep.update({'step-name':'Loop 3'})
            ends = [{'condition':"default",'goto':do3,'edgeidx':str(edgeididx)}]
            edgeididx=edgeididx+1
            otherEnds = testStep['Ends']['EndEntry']
            condition = otherEnds['EndType']+otherEnds['Oper']+otherEnds['Value']
            goto = int(otherEnds['Step'])
            ends.append({'condition':condition,'goto':goto,'edgeidx':str(edgeididx)})
            edgeididx=edgeididx+1
            thisStep.update({'ends':ends})
        elif stepType=='Loop 4':
            thisStep.update({'step-name':'Loop 4'})
            ends = [{'condition':"default",'goto':do4,'edgeidx':str(edgeididx)}]
            edgeididx=edgeididx+1
            otherEnds = testStep['Ends']['EndEntry']
            condition = otherEnds['EndType']+otherEnds['Oper']+otherEnds['Value']
            goto = int(otherEnds['Step'])
            ends.append({'condition':condition,'goto':goto,'edgeidx':str(edgeididx)})
            edgeididx=edgeididx+1
            thisStep.update({'ends':ends})
        elif stepType=='End':
            thisStep.update({'step-name':'end'})
            thisStep.update({'ends':[]})
        graphDict.append(thisStep)
    return graphDict

    
Procedure.convert_to_graph_dict = convert_to_graph_dict

def vizualize(self):
    self.graphDict = self.convert_to_graph_dict()
    app = dash.Dash(__name__)
    directed_elements = [{'data':{'id':str(step['_id']),'label':step['step-name']}} for step in self.graphDict]
    directed_edges = []
    for step in self.graphDict:
        edges = [{'data':{'id':end['edgeidx'],'label':end['condition'],'source':str(step['_id']),'target':str(end['goto'])}} for end in step["ends"]]
        directed_edges = directed_edges+edges
    directed_elements = directed_elements+directed_edges
    c = cyto.Cytoscape(
            id='cytoscape-styling-9',
            layout={'name': 'circle'},
            style={'width': '100%', 'height': '1500px'},
            elements=directed_elements,
                stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        # The default curve style does not work with certain arrows
                        'curve-style': 'bezier',
                        'target-arrow-shape':'vee',
                        'target-arrow-color':'blue',
                        'line-color':'blue',
                        'label':'data(label)'
                    }
                },
            ]
            )
    app.layout = html.Div([c])
    app.run_server(debug=True)


Procedure.vizualize = vizualize

