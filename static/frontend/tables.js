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
        console.log("RESOURCES RETURNED:  ", values)
        let bruh = values.resources; 
        for (let i = 0; i < bruh.length; i++) {
            let temper = 0
            if (!((bruh[i]['value'] == 0) && (bruh[i]['always'] == 1))) {
                inventoryValues[i] = []; 
                inventoryValues[i][0] = bruh[i]['name'];
                    if (bruh[i]['integer'] == 0) {
                        inventoryValues[i][1] =  parseFloat(bruh[i]['value']).toFixed(2);
                    } else {
                        inventoryValues[i][1] =  parseFloat(bruh[i]['value']).toFixed(0);
                    }
            }
        }
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