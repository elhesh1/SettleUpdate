 window.onload = function() {
    setGame();
 }


// backendpath = `https://americagame-d4e96c50eefc.herokuapp.com/`
backendpath = `http://127.0.0.1:5000`
async function setGame() { // this sets up all the functions
  

    hoverMap =       {
        'FarmerJobGrid'  : ['FarmerJobToolTip','FarmersToolTipText','Job','farmer',1],
        'HuntersJobGrid' : ['HuntersJobToolTip','HuntersToolTipText','Job','hunter',2],
        'CooksJobGrid' : ['CooksJobToolTip','CooksToolTipText','Job','cook',3],
        'LoggersJobGrid' : ['LoggersJobToolTip','LoggersToolTipText','Job','logger',4],
        'ButchersJobGrid' : ['ButchersJobToolTip','ButchersToolTipText','Job','butcher',11],
        'BuilderJobGrid' : ["BuildersJobToolTip",'BuildersToolTipText','Job','builder',15],
        'topFoodBar' : ['HealthToolTip','HealthToolTipText' , 'Value'],
        'RationGrid' : ['RationToolTip', 'RationToolTipText', 'Value'],
        'Strength' : ['StrengthToolTip','StrengthToolTipText', 'Value'],
        'TownHallBuildGrid' : ['TownHallToolTip','TownHallToolTipText', 'Value', '.TownHall'], 
        'peopleSupply' : ['peopleSupplyToolTip','peopleSupplyToolTipText', 'Supply','peopleSupply'],
        'toolSupply' : ['toolSupplyToolTip','toolSupplyToolTipText', 'Supply','toolSupply'],
        'resourceSupply' : ['resourceSupplyToolTip','resourceSupplyToolTipText', 'Supply','resourceSupply'],
        'EnglandExplanation' : ['englandExplanationToolTip', 'englandExplanationToolTipText', 'other', 'EnglandExplanation'],
        'HealthGrid2' :  ['HealthToolTip','HealthToolTipText' , 'Value'],
        'PlantedGrid' : ['PlantedToolTip', 'PlantedToolTipText', 'Value', 'PlantedGrid'],
        'ToolShopBuildGrid' : ['ToolShopToolTip', 'ToolShopToolTipText','Value', '.ToolShop']
    }
    logCabinCapacity = 4


    await buildingSetUp() /// and country set up
    var slider = document.getElementById("myRange");
    var sliderValueElement = document.getElementById("sliderValue");
    sliderValueElement.textContent = slider.value;
    slider.addEventListener("input", function() {
      sliderValueElement.textContent = slider.value;
    });
    BuildingChange =  new Map();

    const buttons = document.querySelectorAll('.B');      // these are the buttons that + or - for jobs     
        buttons.forEach(button => {
        button.addEventListener('click', buttonAction);
    });
    const nextW = document.getElementById('NextW');                 
    nextW.addEventListener('click', async function() {
        nextW.disabled = true; 
        try {
            await advance(); 
        } catch (error) {
            console.error('Error:', error);
        } finally {
            nextW.disabled = false; 
        }
    });
    const AdjustB = document.querySelectorAll('.Adjust');       // these are the buttons that control how many people are added for a job button ('.B')
        AdjustB.forEach(AdjB => {
            AdjB.addEventListener('click',changeValueOfInputForJobs);
        });

     document.getElementById('Clear').addEventListener('click', clearJobs);

    const buttonsB = document.querySelectorAll('.BuildingButton');                
        buttonsB.forEach(buttonB => {
            console.log("SETTING UP BB")
        buttonB.addEventListener('click', buttonActionBuilding);
        });
    // const buttonsBW = document.querySelectorAll('.BuildingButtonWorkers');                
    //     buttonsBW.forEach(buttonBW => {
    //     buttonBW.addEventListener('click', buttonActionBuildingWorkers);
    //     });
    // reset.addEventListener('click', resett2);
    // const buttonsBU= document.querySelectorAll('.BuildUpgrade');                
    //     buttonsBU.forEach(buttonBU => {
    //     buttonBU.addEventListener('click', buttonActionBuildingUpgrade);
    //     });
    // reset.addEventListener('click', resett2);


    const buttons3 = document.querySelectorAll('.jobGrid');            
        buttons3.forEach(button3 => {
        button3.addEventListener('mouseover', toggleHover,false);
        button3.addEventListener('mouseleave', toggleHoverOff,false);
        });
    const buttons4 = document.querySelectorAll('.BuildingGrid');                
        buttons4.forEach(button4 => {
        button4.addEventListener('mouseover', toggleHover,false);
        button4.addEventListener('mouseleave', toggleHoverOff,false);
        });  
        
    // getQueue();
    // reset.addEventListener('click', resett2);
    // document.getElementById('InventoryT').click();      //              ///////// Opening Tab ///////////////
    // await showValues();

    const buttons5 = document.querySelectorAll('.Hover');                
    buttons5.forEach(button5 => {
    button5.addEventListener('mouseover', toggleHover,false);
    button5.addEventListener('mouseleave', toggleHoverOff,false);
    });  
    const buttons6 = document.querySelectorAll('.HoverSupply');
    buttons6.forEach(button6 => {
    button6.addEventListener('mouseover', toggleHover,false);
    button6.addEventListener('mouseleave', toggleHoverOff,false);
    }); 
    let reset = document.getElementById('reset');
    reset.addEventListener('click', resett);

}

function changeValueOfInputForJobs() { // these are the buttons that control how many people are added for a job button ('.B')
    id = this.id
    console.log("you clicked this:  ", id)
    console.log()
    setVal('job_modifier',{value: jobMulti[id] } )

    const AdjustB = document.querySelectorAll('.Adjust');
        AdjustB.forEach(AdjB => {
            AdjB.className = AdjB.className.replace(" active", "");
    });

    thisdude = document.getElementById(id);
    thisdude.className += " active";

    return 
}

async function setVal( variable, options, user_id=currUserName = getCookie('userID').split('userID=')[1]) { // change the value for a specific user
    const data = {};
    for (let key in options) {
        if (options[key] !== null && options[key] !== undefined) {
            data[key] = options[key];
        }
    }
    try {     
        const response = await fetch(backendpath + `/set/${user_id}/${variable}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  
        });
        if (!response.ok) {     // not good :(
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const responseData = await response.json();
    } catch (error) {       // did not work
        console.error('There was a problem with your fetch operation:', error);
    }
}

async function changeVal(user_id, variable, options) { // change the value for a specific user
    const data = {};
    for (let key in options) {
        if (options[key] !== null && options[key] !== undefined) {
            data[key] = options[key];
        }
    }
    try {     
        const response = await fetch(backendpath + `/change/${user_id}/${variable}`, {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),  
        });
        if (!response.ok) {     // not good :(
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const responseData = await response.json();
    } catch (error) {       // did not work
        console.error('There was a problem with your fetch operation:', error);
    }
}

async function getVal( variableName, currUserName = getCookie('userID').split('userID=')[1]) {
    try {
        const response = await fetch(backendpath + `/get/${currUserName}/${variableName}`, {
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
        const value = data[variableName];
        return value;

    } catch (error) {
        console.error('Error fetching resource:', error);
        alert(`Error: ${error.message}`);
    }
}

async function resett(newV=0) {     // function from resett it is used 
    console.log("RESETTING")
    document.getElementById("Season").textContent = "Spring";
    // document.getElementById('One').click();
    // const requestSupply = document.querySelectorAll('.requestSupply');
    // requestSupply.forEach(rs => {
    //     rs.className = rs.className.replace(" active", "");
    // });

 //   await tabReset();
    currUserName = getCookie('userID').split('userID=')[1]
    console.log(" Going to reset this user---    ::::::  ", currUserName)
    try {
         const response = await fetch(backendpath + `/reset/${currUserName}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userName: currUserName,
                    newV: newV
                }),            });
            const responseData = await response.json();
        }
        catch (error) {       // did not work
            console.error('Error BROKE BROKE:', error);
        }
        Object.keys(labelMap).forEach(key => {
            if (labelMap[key][1] == 'JOB') {
                getVal(labelMap[key][3]) 
                .then(value => {
                    document.getElementById(labelMap[key][0]).innerText = value;
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    document.getElementById(labelMap[key][0]).innerText = 'Error fetching data';
                });
            }
    
        });
        document.getElementById('A').innerText = '50'; // hardcode :(
        tableMaker()  
    // .then(() => {
    //     getQueue()
    //     buildingsShowing()
         tabSetUp()
    // })
    // .catch(error => {
    //     console.error('Error updating data:', error);
    // });

}



async function buttonAction() { 
    let id = this.id
    let jobID = buttonMap[id][0]
    let type = labelMap[jobID][0]
    let varName = labelMap[jobID][3]
    userName = getCookie('userID').split('userID=')[1]
    changeVal(userName, varName,{value: buttonMap[id][1] } ) // updates in db
    .then(() => {                           // retrieves val from db
        getVal(varName)
            .then(value => {
                document.getElementById(type).innerText = value;    
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                document.getElementById(type).innerText = 'Error fetching data';
            });
        getVal('Available_value')
            .then(value => {
                document.getElementById('A').innerText = value;
                tooltipSetupBuilding(hoverMap[labelMap[jobID][2]])
            })
            .catch(error => {
                console.error('Error fetching data for jobID 6:', error);
                document.getElementById('A').innerText = 'Error fetching data';
            });
    })
    .catch(error => {
        console.error('Error updating data:', error);
    });
}


async function getAllUsers() {
    try {
        const response = await fetch(backendpath + `/user`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data.value;
    } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
        throw error;
    }
}


document.addEventListener('DOMContentLoaded', async (event) => {

    cookies = getCookie()
    console.log("COOKIES  ", cookies)
    if (cookies.includes("userID")) {
        console.log("Already set this one up")
    }
    else {
        console.log("set up a new cookie")
        uu = generateUUID()
        setCookie('userID', uu, 365)
        
    }
    // set up a new 
    console.log("Test1")

    cookie = getCookie()
    cookie = cookie.split('userID=')[1]
    console.log("COOKIE  ::::   ", cookie)
    const response = await fetch(backendpath + `/add_user/${cookie}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    });
    const responseData = await response.json();
   // countrySetUpNative();
});

function getCookie() {
    let decodedCookie = decodeURIComponent(document.cookie);
    return decodedCookie;
}

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = `${cname}=${cvalue};${expires};path=/`;
}

function generateUUID() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

async function openTab(id, value) {
    tabcontent = document.getElementsByClassName("tabcontent"); // hid all other Tabs doggg
    for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
    }
    document.getElementById(value).style.display = "grid"

    activeTab = id;
    tabB = document.getElementsByClassName("tabB");
    for (i = 0; i < tabB.length; i++) {
        tabB[i].className = tabB[i].className.replace(" active", "");
    }
    if (id == 'FoodT') {
        foodTabSetUp();
    }
    else if (id == 'BuildingsT') {
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
    thisdude = document.getElementById(id);
    thisdude.className += " active";
}

async function clearJobs() {
    const response = await fetch(backendpath + `/clearJobs/${currUserName}`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),  
    })
        for (let key in labelMap) {
            if( labelMap[key][1] == "JOB") {
                jobb = document.getElementById(labelMap[key][0]);
                jobb.innerText = 0;
            }
        }
    let av = await getVal('Available_value')
    aval = document.getElementById('A');
    aval.innerText = av
}

async function buildingSetUp() {
     
    let buildings = await fetchBuildingCostMap();
    buildings = buildings['buildings']
 
    for (const details of Object.values(buildings)) {
        if (details['typeOfBuilding'] === "Housing") {
            await buildingSetUpInner(details);
        }
    }

    for (const details of Object.values(buildings)) {
        if (details['typeOfBuilding'] === "Raw Material Maker") {
            await buildingSetUpInner(details);
        }
    }

    // Second loop
    for (const details of Object.values(buildings)) {
        if (details['typeOfBuilding'] === "Second Level") {
            await buildingSetUpInner(details);
        }
    }
     return
}


//const buildingNames = {} // id to Name. This is set up automatically  - may be obsolete
//const namesBuilding = {} // fullname -> array with first element ID

async function buildingSetUpInner(values) {
    let nameB = values['name']
    let fullName = nameB.replace(/_/g, " ")
    if (values['work'] > 0 ) {
        let type = values['typeOfBuilding']
        hoverMap[nameB + 'BuildGrid'] = [nameB + 'ToolTip', nameB + 'Inner', type, nameB, 'PLACEHOLDER'];
        let string = '<div class="BuildingGrid" id = "'  + nameB + 'BuildGrid"><h5 class="BuildingTitle" id="' + nameB + '">' + fullName + '</h5><button class="BuildingButtonUp BuildingButton '+ nameB + '" >+'
        string += '</button> <button class="BuildingButtonDown BuildingButton '+ nameB + '" >-</button><h5 class="BuildingNumberCurrent"  id="'+ nameB + 'Current">0</h5>'
        if(type != "Housing") {
            string += '<h5 class="BuildingpeopleWorking"  id="' + nameB + 'peopleWorking' +  '">' +  values['workers'] + '</h5>'
            string += '<h5 class="slash"  id="' + nameB + 'peopleWorking' +  '">' + '/'+ '</h5>'
            string += '<h5 class="BuildingpeopleCap"  id="' + nameB + 'peopleCap' +  '">' +  values['max'] + '</h5>'
            string += '<button class="BuildingButtonWorkersUp BuildingButtonWorkers '+ nameB + '" >+</button>'
            string += '<button class="BuildingButtonWorkersDown BuildingButtonWorkers '+ nameB + '" >-</button>'

        }
        string += '<h5 class="BuildingNumberAlreadyBuilt"  id="' + nameB + 'currently' +  '">0</h5></div>'
        const nextW = document.getElementById('building-flex-container');
        nextW.innerHTML += string; 
        let hoverString = '<span class="jobToolTip" id="'+ nameB + 'ToolTip">'   
        hoverString += '<h5 class="ToolTipTitle">'+ fullName + '</h5>'
        hoverString += '<h3 class="ToolTipText" id="' + nameB + 'ToolTipText">' + type + '</h3>'
        hoverString += '<div class="flex-container" id="'+ nameB + 'Inner"></div></span>'
        const grid = document.getElementsByClassName('grid-container')[0];
       grid.innerHTML += hoverString
    }
    return
}


function buttonActionBuilding() {
    let buildingType = this.className.split(' ')[2];
    let changeName = buildingType += 'Current'
    changeNumber = 1
    if (this.className.includes('BuildingButtonDown')) {
        changeNumber = -1;
    }


    if (!BuildingChange.has(buildingType)) {
        BuildingChange.set(buildingType, [0]);
    }
    let currentValue = BuildingChange.get(buildingType);
    currentValue[0] += changeNumber;
    if (currentValue[0] < 0) {
        currentValue[0] = 0;
    }
    BuildingChange.set(buildingType, currentValue);


    const newval = BuildingChange.get(buildingType)[0]; 
    const element = document.getElementById(changeName);
    
    if (element) {
        element.innerText = newval;  
    } else {
        console.error("Element with id:", changeName, "not found.");
    }
    

}