async function foodTabSetUp() {
    userName = getCookie('userID').split('userID=')[1]
    document.getElementById('StrengthB').innerText = await getVal('Strength')
    let plantedcount = await getVal('Planted');
    document.getElementById('Planted').innerText = parseFloat(plantedcount).toFixed(2);
    foodParagraphHelper();
}


async function buildingTabSetUp() { 
    userName = getCookie('userID').split('userID=')[1]
    pop = await getVal('Population')
  
    housed = await getVal('Log_Cabin') * 4  // 
    housingvalue = document.getElementById('HousingValue');
    string = 'Housing Provided: '+ housed + ' / ' + pop;
    housingvalue.innerText = string;
    
    const response = await fetch(backendpath + `/buildings/${currUserName}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'An unknown error occurred');
    }
    const data = await response.json();
    let buildings = data['buildings']


  //  console.log("BUILDINGS IN THE BUILDING TAB SET UP TYPE SHIT  ",  buildings)
    a = document.getElementById('TownHallcurrently');
    a.innerText = buildings['Town_Hall']['value'];

    b = document.getElementById('ToolShopcurrently');
    b.innerText = buildings['Tool_Shop']['value'];

    c = document.getElementById('Log_Cabincurrently');
    c.innerText = buildings['Log_Cabin']['value'];

    d = document.getElementById('Clay_Pitcurrently');
    d.innerText = buildings['Clay_Pit']['value'];

    e = document.getElementById('Minecurrently');
    e.innerText = buildings['Mine']['value'];

    f = document.getElementById('Forgecurrently');
    f.innerText = buildings['Forge']['value'];

    g = document.getElementById('Kilncurrently');
    g.innerText = buildings['Kiln']['value'];
    await buildingsShowing();
}

async function inventoryTabSetUp() {
    tableMaker();
}

async function tabReset() {

    if (activeTab == 'BuildingsT') {
        //BuildingpeopleWorkin
    }
    if (activeTab == 'CountriesT') {
        console.log("COUNTRIE T ACTIVATED")
    }

}

async function tabSetUp() {
    if (activeTab == 'FoodT') {
        foodTabSetUp();
    }
    else if (activeTab == 'BuildingsT') {
        await buildingTabSetUp();
    }
    else if (activeTab == 'InventoryT'){
        inventoryTabSetUp();
    }
    else if (activeTab == 'CountriesT') {
        countrySetUp()
    }
    else if(activeTab == 'FactoryT') {
        factorySetUp()
    }
}

async function buildingsShowing() {
   // let buildingshift = await fetchBuildingshift();
    let buildings = await fetchBuildingCostMap();
    let currentlyWorkings = document.getElementsByClassName("BuildingpeopleWorking"); // actually keep this one out
   // console.log("curr working  ", currentlyWorkings)



    for (i = 0; i < currentlyWorkings.length; i++) {        // have to adjust that minus one i think you know whats up ;)
        // console.log(currentlyWorkings[i])
        // console.log("chat is this real ", currentlyWorkings[i].innerText)
        // console.log(buildings.buildings)
        // console.log(namesBuilding)
        // console.log(namesBuilding[currentlyWorkings[i].id.replace('peopleWorking', '')][0]-1)
        // console.log(buildings.totOffset)
     //   console.log(currentlyWorkings[i])
        let elementId = currentlyWorkings[i].id;
        let jobName = elementId.split("people")[0];
        //console.log(currentlyWorkings[i], "    ", buildings['buildings'][jobName]['workers'] )

        currentlyWorkings[i].innerText = buildings['buildings'][jobName]['workers'];
    }


    let capWorkings = document.getElementsByClassName('BuildingpeopleCap');
    for (i = 0; i < currentlyWorkings.length; i++) {
        let elementId = capWorkings[i].id;
        let jobName = elementId.split("people")[0];
      //  console.log(capWorkings[i], "    ", buildings['buildings'][jobName]['max'] )

        capWorkings[i].innerText = buildings['buildings'][jobName]['max'];
    }  
}

async function factorySetUp() {
    currUserName = getCookie('userID').split('userID=')[1]

    const response = await fetch(backendpath + `/factoryTab/${currUserName}`);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    inner = document.getElementById('FactoryFlex')
    inner.innerHTML =  data['string']

    let buttons2 = document.querySelectorAll('.TradeButton');
    buttons2.forEach(button2 => {
        button2.addEventListener('click', tradeButton);
    });
}

async function foodParagraphHelper() {
    let pop = await getVal('Population')
    let fp = document.getElementById('FoodParagraph')
    let totNeeded = Math.round(pop * 0.2) / 10
    let string =  "Every citizen needs 0.02 food a week to be fully fed. With a population of " + pop + ", " + totNeeded + " food is needed every week to keep them at full strength";
    fp.innerText = string;
}