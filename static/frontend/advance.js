
async function advance() {   
    currUserName = getCookie('userID').split('userID=')[1]
    inputs = []
    

    await addBuildings(BuildingChange)
    if (activeSupplyType != undefined) { // active supply type is the supply type from England
        console.log(" BRUH 300000 ", activeSupplyType)
        const response = await fetch(backendpath + `/activeSupplyType/${currUserName}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({activeSupplyType}),  
        });
        activeSupplyType=undefined
    }


    //     method: 'POST', 
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(inputs),  
    // });
    
    // if (!response1.ok) {
    //     throw new Error(`HTTP error! Status: ${response1.status}`);
    // }
    // const data1 = await response1.json();


    // const currents = document.getElementsByClassName('BuildingNumberCurrent');
    //         for (let i = 0; i < currents.length; i++) {
    //     currents[i].textContent = 0;
    // }

    // BuildingChange = {}

    await advanceJob();              // do jobs // make sure to reset building queue ids
    await getQueue();
    const response = await fetch(backendpath + `/advancePackage/${currUserName}`); 
    const data = await response.json();
    let w = data['week'];  
    document.getElementById("W").textContent = w;
    if(w == 1) {
        let s = data['season']
        switch(s) { 
            case 1:
                document.getElementById("Season").textContent = "Spring"; break;
            case 2:
                document.getElementById("Season").textContent = "Summer";  break; 
            case 3:
                document.getElementById("Season").textContent = "Fall"; break;
            case 0:
                document.getElementById("Season").textContent = "Winter"; 
                let y = data['year']
                document.getElementById("Year").textContent = y; 
                break;

        }
    }
    document.getElementById("P").textContent = data['Population']
    console.log("THIS IS THE DATA ", data)
    // A = data.contacts[6-1].value
    // if (A < 1) {
    //     let newValuesToPutIn = await getContacts();
    //     newValuesToPutIn = newValuesToPutIn['contacts']
       document.getElementById('F').innerText = data['F']
        document.getElementById('H').innerText = data['H']
        document.getElementById('C').innerText = data['C']
         document.getElementById('L').innerText = data['L']
        document.getElementById('B').innerText = data['B']
      document.getElementById('W2').innerText = data['W2']
    document.getElementById("A").textContent = data['A']

    document.getElementById("Clay_PitpeopleWorking").textContent = data['CPW']
    document.getElementById("ForgepeopleWorking").textContent = data['FW']
    document.getElementById("MinepeopleWorking").textContent = data['MW']
    document.getElementById("KilnpeopleWorking").textContent = data['KW']

    var elements = document.getElementsByClassName("HealthN");
    if (elements.length > 0) {
        elements[0].innerText = data['Health'];
        elements[1].innerText = data['Health'];
    }

    if (activeTab == 'FoodT') {
        foodTabSetUp();
    }
    else if (activeTab == 'BuildingsT') {
             /// will have to update this perhaps
        await buildingTabSetUp();
    }
    else if (activeTab == 'InventoryT'){
        inventoryTabSetUp();
    }
    else if (activeTab == 'CountriesT') {
        countrySetUp()
    }
    // document.getElementById('StrengthB').innerText = await getValue('contact/',18)
    
    // var leveldButtons = document.getElementsByClassName("levelButton");
    // i = 0
    // while (leveldButtons.length > i) {
    //     leveldButtons[i].className = leveldButtons[i].className.replace(" active", "").trim();
    //     i++;
    // }
    

    // const buttons5 = document.querySelectorAll('.HoverSupply');
    // buttons5.forEach(button5 => {
    // button5.addEventListener('mouseover', toggleHover,false);
    // button5.addEventListener('mouseleave', toggleHoverOff,false);
    // }); 

    const buildingQNumbers = document.querySelectorAll('.BuildingNumberCurrent');
    buildingQNumbers.forEach(element => {
        console.log('kmon mang')
        element.innerText = '0';
    });
   
    BuildingChange =  new Map();
    await buildingsShowing() 
}

async function advanceJob() {
    await setVal('RationP', {value : parseInt(document.getElementById("sliderValue").textContent)})
    const response = await fetch(backendpath + `/advance/${currUserName}`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify([]),  
    });

 
}

async function addBuildings(buildingChange) {
    console.log("adding building bruh  " , buildingChange)
    const dataQ = {};
    console.log(typeof buildingChange)
    buildingChange.forEach((value, key) => {
        dataQ[key] = value;
    });

    const response = await fetch(backendpath + `/${currUserName}/buildings/addQueue`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({dataQ})  
    });
    const data = await response.json();
    console.log("RESPONSE " , data)
}