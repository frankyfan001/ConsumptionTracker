import React, {useState} from 'react';
import './App.css';
import {Form, Radio} from 'semantic-ui-react'
import {parseData, PieChartFigure} from "./Analysis";


function getPartitionData(node: any) {
    var partition = [
        ['Heap Partition of Local Variables in ' + node.name, 'Percentage', {
            role: "tooltip",
            type: "string",
            p: {html: true}
        }],
    ]

    var typed_memory = node.heapAlloc.total.typed_memory
    var i
    for (i = 0; i < typed_memory.length; i += 1) {
        partition.push([
            typed_memory[i]["type"],
            typed_memory[i]["value"],
            typed_memory[i]["variables"]])
    }
    return partition
}


const LargestConsumption = (largestFrames: any) => {
    const [radioValue, setRadioValue] = useState('1');
    const [methodData, setMethodData] = useState(getPartitionData(largestFrames[0].data))

    var k
    for (k = 0; k < largestFrames.length; k += 1) {
        parseData(largestFrames[k].data)
    }

    function onchange(e: any, {value}: any) {
        setRadioValue(value)

        var i
        for (i = 0; i < largestFrames.length; i += 1) {
            if (value === largestFrames[i].value) {
                setMethodData(getPartitionData(largestFrames[i].data))
            }

        }
    }


    return (
        <div>
            <Form>
                <Form.Field>
                    <b>Below are the top memory consumption frames (ordered by size). Please select the one you are interested in</b>
                </Form.Field>
                {largestFrames.map((radio: any, idx: any) => {
                    return (
                        <Form.Field>
                            <Radio
                                label={radio.name}
                                name={radio.value}
                                value={radio.value}
                                checked={radioValue === radio.value}
                                onChange={onchange}
                            />
                        </Form.Field>
                    )
                })}

            </Form>
            <PieChartFigure partition={methodData}></PieChartFigure>
        </div>
    )
        ;
}


export default LargestConsumption;