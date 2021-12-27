import React, {FunctionComponent} from 'react';
import './App.css';
import {InfoIconWithTooltip} from 'icon-with-tooltip';
const {FlameGraph} = require('react-flame-graph');
const {Chart} = require('react-google-charts');


var smallestConsumption:number
var largestConsumption:number

function getSmallestAndLargestConsumption(currentNode:any) {
    smallestConsumption = Math.min(smallestConsumption, currentNode.heapAlloc.total.total_memory)
    largestConsumption = Math.max(largestConsumption, currentNode.heapAlloc.total.total_memory)

    var i, currChild
    if ("children" in currentNode) {
        for (i = 0; i < currentNode.children.length; i += 1) {
            currChild = currentNode.children[i];
            getSmallestAndLargestConsumption(currChild);
        }
    }
}

export function parseData(currentNode:any) {

    // In the flame graph, greener color refers to lower memory consumption, while redder color refers to higher memory consumption
    const colorSequence = ["#fc432a", "#f5572b", "#e7722d", "#d8882f", "#cd9530", "#c79b31", "#c0a132", "#baa733", "#b1ae35", "#a6b536", "#9abd38", "#8bc539", "#73cf3c", "#52d93f"]
    var index
    if (largestConsumption === smallestConsumption) index = 13
    else index = (13 - (currentNode.heapAlloc.total.total_memory - smallestConsumption)/(largestConsumption - smallestConsumption)*13) | 0

    currentNode["backgroundColor"] = colorSequence[index];

    if ("heapAlloc" in currentNode && "vars" in currentNode.heapAlloc && "total" in currentNode.heapAlloc && typeof currentNode.heapAlloc.total =='object'
        && "typed_memory" in currentNode.heapAlloc.total) {

        var variables = currentNode.heapAlloc.vars
        var typed_memory = currentNode.heapAlloc.total.typed_memory

        var j, currType

        for (j = 0; j < typed_memory.length; j += 1) {
            currType = typed_memory[j].type;
            var variables_under_type = []
            var k
            for (k = 0; k < variables.length; k += 1) {
                if (variables[k].type === currType) variables_under_type.push(variables[k])
            }
            variables_under_type.sort((v1, v2) => (v2.value - v1.value))

            var m
            var variable_str = ""

            for (m = 0; m < variables_under_type.length; m += 1) {
                variable_str += "\n" + variables_under_type[m].name + ": " + variables_under_type[m].value + " bytes"
            }

            typed_memory[j]["variables"] = variable_str
        }
    }


    if (!currentNode.name.includes("memory consumption")) {
        currentNode["nameTemp"] = currentNode.name
        var runtime = (Math.round(currentNode.value *1000 * 100000) / 100000).toFixed(5);
        currentNode["name"] = currentNode.name + " ( memory consumption:" + currentNode.heapAlloc.total.total_memory + " bytes, runtime: " + runtime + "ms)"
    }


    var i, currChild
    if ("children" in currentNode) {
        for (i = 0; i < currentNode.children.length; i += 1) {
            currChild = currentNode.children[i];
            parseData(currChild);
        }
    }
}

const Analysis = (data:any) => {

    if ("data" in data) data = data.data

    smallestConsumption = data.heapAlloc.total.total_memory
    largestConsumption = smallestConsumption
    getSmallestAndLargestConsumption(data)
    parseData(data)

    const initialState = [] as any
    const [partitionData, setPartitionData] = React.useState(initialState)

    return (
        <div className="App">
            <header className="App-white">
                <FlameGraph
                    data={data} // TODO: add background color to each frame node, the higher memory the heavier color
                    height={300}
                    width={1300}
                    onChange={(node: any) => {
                        var partition =[
                                ['Heap Partition of Local Variables in ' + node.source.nameTemp, 'Percentage', { role: "tooltip", type: "string", p: { html: true } }],
                            ]

                        var typed_memory = node.source.heapAlloc.total.typed_memory
                        var i
                        for (i = 0; i < typed_memory.length; i += 1) {
                            partition.push([
                                typed_memory[i]["type"],
                                typed_memory[i]["value"],
                                typed_memory[i]["variables"]])
                        }

                        setPartitionData(partition)


                    }}
                />
            </header>
            <InfoIconWithTooltip text="Note: The heap partition only includes the variables allocated in the current stack frame but not all the variables in the child frames. If we have function call a() in another function def b(), the frame for b will not have the memory consumption for variables in a" placement="top" />
            <PieChartFigure partition={partitionData}></PieChartFigure>

        </div>

    );
}


interface PieProp {
    partition: any,
}

export const PieChartFigure: FunctionComponent<PieProp> = ({partition}) => {

    if (partition.length === 0) return (<div/>)
    return (
        <div className="App-white">
        <Chart
            chartType="PieChart"
            width="70%"
            height="400px"
            data={partition}
            options={{
                pieSliceText: 'label',
                title: partition[0][0],
                annotations: {
                    textStyle: {color: '#FFFFFF'},
                    tooltip: { isHtml: true, trigger: "visible" }
                }
            }}
            legendToggle
        />
        </div>
                )
}



export default Analysis;