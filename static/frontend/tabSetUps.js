async function foodTabSetUp() {
    userName = getCookie('userID').split('userID=')[1]
    document.getElementById('StrengthB').innerText = await getVal('Strength')
    foodParagraphHelper();

}

async function buildingTabSetUp(pop, h) { 
    userName = getCookie('userID').split('userID=')[1]
    if (pop == -1) {  pop = await getValue('Population');}
    h = await getBuilding(1) 
    housed = h['buildingInfo'].value * h['buildingInfo'].capacity
    housingvalue = document.getElementById('HousingValue');
    string = 'Housing Provided: '+ housed + ' / ' + pop;
    housingvalue.innerText = string;
    
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

function tabSetUp() {
    if (activeTab == 'FoodT') {
        foodTabSetUp();
    }
    else if (activeTab == 'BuildingsT') {
        buildingTabSetUp(-1, -1);
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
        currentlyWorkings[i].innerText = buildings.buildings[namesBuilding[currentlyWorkings[i].id.replace('peopleWorking', '')][0]-1-buildings.totOffset ]['working']['value'];
    }
    let capWorkings = document.getElementsByClassName('BuildingpeopleCap');
    for (i = 0; i < currentlyWorkings.length; i++) {
        capWorkings[i].innerText =buildings.buildings[namesBuilding[currentlyWorkings[i].id.replace('peopleWorking', '')][0]-1-buildings.totOffset]['working']['maximum'];
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