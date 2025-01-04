
async function advance() {   
    currUserName = getCookie('userID').split('userID=')[1]
    console.log("Advancing", currUserName)
    inputs = []
    // if (activeSupplyType != undefined) {
    //     console.log(" BRUH 300000")
    //     const response = await fetch(backendpath + `/activeSupplyType/${currUserName}`, {
    //         method: 'PATCH', 
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({activeSupplyType}),  
    //     });
    //     activeSupplyType=undefined
    // }

    //   for (const build in BuildingChange) {
    //     inputs.push({ 'name': build, 'value': BuildingChange[build][0], 'level' : BuildingChange[build][1] });
    //   }
    // const response1 = await fetch(backendpath + `/addCurr/${currUserName}`, {

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

    await advanceJob();              // do jobs

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
    // A = data.contacts[6-1].value
    // if (A < 1) {
    //     let newValuesToPutIn = await getContacts();
    //     newValuesToPutIn = newValuesToPutIn['contacts']
    //     document.getElementById('F').innerText = newValuesToPutIn[1-1]['value']
    //     document.getElementById('H').innerText = newValuesToPutIn[2-1]['value']
    //     document.getElementById('C').innerText = newValuesToPutIn[3-1]['value']
    //     document.getElementById('L').innerText = newValuesToPutIn[4-1]['value']
    //     document.getElementById('B').innerText = newValuesToPutIn[11-1]['value']
    //     document.getElementById('W2').innerText = newValuesToPutIn[15-1]['value']
    // }
    // document.getElementById("A").textContent = A

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
        buildingTabSetUp(data.contacts[5-1].value);
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
    // await buildingsShowing() 

    // const buttons5 = document.querySelectorAll('.HoverSupply');
    // buttons5.forEach(button5 => {
    // button5.addEventListener('mouseover', toggleHover,false);
    // button5.addEventListener('mouseleave', toggleHoverOff,false);
    // }); 


    // let exdays = 365
    // let uniqueId = generateUUID();

    // let cname = "name"
    // setCookie(cname, uniqueId, exdays)

    // let cookies = getCookie()

    // console.log("COOKIE:  ", cookies)
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

