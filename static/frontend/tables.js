function tableMaker() { 
    takeInventory()
    .then(iv => {
        let updatedTableHtml = makeTable(iv); 
        tableContainer.innerHTML = updatedTableHtml; 
    })
    .catch(error => {
        console.error("Error in tester:", error);
    });
}

async function takeInventory() {
    let inventoryValues = []; 
    try {
        let values = await getResources(); 
        let bruh = values.resources; 
        console.log( bruh)
        i = 0
        Object.keys(bruh).forEach(key => {
            const resource = bruh[key];
            if(resource['type'] == 'food') {
                if (!((resource['value'] == 0) && (resource['always'] == 1))) { // 0s are always shown
                    inventoryValues[i] = []; 
                    inventoryValues[i][0] = key.replace(/_/g, ' ');
                    if (resource['integer'] == 0) {  // 1s are integers
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(2);
                    } else {
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(0);
                    }
                    i = i + 1;
                }

            }
        });
        inventoryValues[i] = []; 
        i = i + 1;
        Object.keys(bruh).forEach(key => {
            const resource = bruh[key];
            if(resource['type'] == 'raw') {
                if (!((resource['value'] == 0) && (resource['always'] == 1))) { // 0s are always shown
                    inventoryValues[i] = []; 
                    inventoryValues[i][0] = key.replace(/_/g, ' ');
                    if (resource['integer'] == 0) {  // 1s are integers
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(2);
                    } else {
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(0);
                    }
                    i = i + 1;
                }

            }
        });
        Object.keys(bruh).forEach(key => {
            const resource = bruh[key];
            if(resource['type'] == 'adv') {
                if (!((resource['value'] == 0) && (resource['always'] == 1))) { // 0s are always shown
                    inventoryValues[i] = []; 
                    inventoryValues[i][0] = key.replace(/_/g, ' ');
                    if (resource['integer'] == 0) {  // 1s are integers
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(2);
                    } else {
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(0);
                    }
                    i = i + 1;
                }

            }
        });
        inventoryValues[i] = []; 
        i = i + 1;
        Object.keys(bruh).forEach(key => {
            const resource = bruh[key];
            if(resource['type'] == 'tool') {
                if (!((resource['value'] == 0) && (resource['always'] == 1))) { // 0s are always shown
                    inventoryValues[i] = []; 
                    inventoryValues[i][0] = key.replace(/_/g, ' ');
                    if (resource['integer'] == 0) {  // 1s are integers
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(2);
                    } else {
                        inventoryValues[i][1] =  parseFloat(resource['value']).toFixed(0);
                    }
                    i = i + 1;
                }

            }
        });
            return inventoryValues; 
    } catch (error) {
        console.error("Error in takeInventory:", error);
        throw error; 
    }
}

function makeTable(tabI) { // makes function table
    var result = "<table style='border-collapse: collapse;   font-size: 2vh;  >"; 
    for (var i = 0; i < tabI.length; i++) {
        if (tabI[i] != undefined) {
            result += "<tr style='height: 3vh;'>"; 
            for (var j = 0; j < tabI[i].length; j++) {
                result += "<td style='width: 50vh;'>" + tabI[i][j] + "</td>"; 
            }
            result += "</tr>"; 
        }         
    }
    result += "</table>"; 
    return result; 
}

async function getResources() {
    currUserName = getCookie('userID').split('userID=')[1]
    try {
        const response = await fetch(backendpath + `/resources/${currUserName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();

        return data;
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}

async function fetchBuildingCostMap() {
    currUserName = getCookie('userID').split('userID=')[1]
    try {
        const response = await fetch(backendpath + `/buildings/${currUserName}`);
                if (!response.ok) {
            throw new Error('Network response was not ok');
        }
                const buildingCostMap = await response.json();        
        return buildingCostMap;
    } catch (error) {
        console.error('Error fetching building cost map:', error);
    }
}


function stringQueueToArray(queueString) {
    const items = queueString.split('-');
    const queue = [];

    items.forEach(item => {
        item = item.trim();  
        if (item) { 
            const [order, name, number] = item.split(/\s+/);  
            queue.push([order, name, parseInt(number, 10)]);  
        }
    });

    return queue;
}
async function getQueue() {
    try {
        let response = await fetch(backendpath + `/currentContent/${currUserName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let string = "<table><thead><tr><th>Name</th><th>Value</th><th>  </th><th></th></tr></thead><tbody>";
        const BQueue = await response.json();
        queue = stringQueueToArray(BQueue['queue'])
        console.log("BUILDING Q RIGHT HERE  ", queue)
        let b2 = BQueue['buildingList'] // b2 is just the list of buildings
        let buildings = BQueue['buildings']
        
        for (let i = 0 ; i < queue.length ; i++) {
            console.log(queue[i])
            console.log("THIS IS important it is the buildings", queue[i][1])
        //     console.log(buildingNames)
        //     if (building['type'] === undefined) {
        //         btype = buildingNames[building['name']]
        //         if (building['name'] == 2){
        //             btype = 'Town Hall'
        //         } else if (building['name'] == 7) {
        //             btype = 'Tool Shop'
        //         }
            string += `<tr><td>${queue[i][1].split('Current')[0].replace(/_/g, ' ')}</td><td>${queue[i][2]}</td><td>${' ' }</td></tr>`;

        //     } else {
        //         console.log("BUIDLINGS", b2)



                // numberName = buildings[i]['name']
                // console.log(numberName, "   ", buildingOffset)
                // while( numberName > buildingOffset) {
                //     numberName -= buildingOffset
                //     console.log("NEW NUMBER NAME ", numberName)
                // }
                // numberName -= 1
                // console.log("NUMBER NAME  ; ", numberName)
                // totalWork = b2[numberName]['work'];
                
                // if (totalWork == -1) {
                //     //// get value from lookuptable
                //     totalWork = 5
                // }
                // progress = totalWork-buildings[i]['value'] 
                // string +=  '<tr><td colspan="3"><progress id="file" max="'+ totalWork + '" value="' +progress  +'"></progress></td></tr>';
        //     }
        }






        
        string += "</tbody></table>";
        buildingQueue.innerHTML = string
        console.log("STRING : ", string)
        for (id in b2) {
            let elementtoUpdate = b2[id].name + 'currently';
            // console.log("b2  ", b2)
            // console.log("elementtoTupdate, ", elementtoUpdate)
            document.getElementById(elementtoUpdate).textContent = b2[parseInt(id)]['value']
        }
    } catch (error) {
        console.error('There was a problem coudlnt get the current buildings :', error);
        throw error;
    }
}
