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