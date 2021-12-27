import React from "react";
import {BrowserRouter, Route} from "react-router-dom";
import App from "./App";
import Analysis, {parseData} from "./Analysis";
import LargestConsumption from "./LargestConsumption"
import data from "./data/stacks.json";


var methodFrames: any[] = []

function getFrames(currentNode:any) {
        methodFrames.push(currentNode)
        var i, currChild
        if ("children" in currentNode) {
                for (i = 0; i < currentNode.children.length; i += 1) {
                        currChild = currentNode.children[i];
                        getFrames(currChild);
                }
        }
}


function getLargestFrames(data:any) {
        parseData(data)
        methodFrames = []
        getFrames(data)
        // sort the frames by their memory consumption
        methodFrames.sort((m1, m2) => (m2.heapAlloc.total.total_memory - m1.heapAlloc.total.total_memory))

        var largestFrames: any[] = []

        var i
        // get the top 10 memory consumption methods
        for (i = 0; i < methodFrames.length && i < 10; i += 1) {
                var currentNode = methodFrames[i]
                if (!currentNode.name.includes("memory consumption")) {
                        currentNode["nameTemp"] = currentNode.name
                        var runtime = (Math.round(currentNode.value *1000 * 100000) / 100000).toFixed(5);
                        currentNode["name"] = currentNode.name + " ( memory consumption:" + currentNode.heapAlloc.total.total_memory + " bytes, runtime: " + runtime + "ms)"
                }
                var name = currentNode["name"]
                largestFrames.push({name: (i+1) + ". " + name, value: String(i+ 1), data: methodFrames[i]})
        }
        return largestFrames
}

const AppRouter = () => (
    <BrowserRouter>
        <Route
            exact path="/"
            component={() => App()}
        />
        <Route
            path="/Analysis"
            component={() => Analysis(data)}
        />
        <Route
            path="/LargestConsumption"
            component={() => LargestConsumption(getLargestFrames(data))}
        />
    </BrowserRouter>
);

export default AppRouter;