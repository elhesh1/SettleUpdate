let hoverMap = {}
const hoverState = new Map();
const tooltipInProgress = new Map(); 
 
async function toggleHover() {
  const id = this.id;
  // console.log (" ID ", id)
  // console.log(hoverMap)
  const tab = document.getElementById(hoverMap[id][0]);
  if (tooltipInProgress.get(id)) return;
  if (!hoverState.has(id) || hoverState.get(id) === 0) {
    tab.style.visibility = 'visible';
    hoverState.set(id, 1);
    tooltipInProgress.set(id, true);
    try {
      await tooltipSetupBuilding(hoverMap[id]);
    } catch (error) {
      console.error("Error setting up tooltip:", error);
    } finally {
      tooltipInProgress.set(id, false);
    }
  } 
}

async function toggleHoverOff() {
  const id = this.id;
  const tab = document.getElementById(hoverMap[id][0]);

  if (hoverState.has(id) && hoverState.get(id) === 1) {
    tab.style.visibility = 'hidden';
    hoverState.set(id, 0);
    if (!tooltipInProgress.get(id)) {
      tab.style.visibility = 'hidden';
    }
  } 
}

async function tooltipSetupBuilding(map) {
  //console.log("MAPPPPP  ", map)
    let cost = document.getElementById(map[1]);
    string = ''
    string +='<div class="flexitem ToolTipLine" width="80%" size="4"></div>'  //line
    string +='<div class="flexitem" id="Cost" style="text-align: center">' + map[2] + '</div>'    // type of item
    string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>'                      // line
    if (map[0] == 'HealthToolTip') {
      string += await hoverString('health');
    } 
    else if (map[0] == 'RationToolTip') {
      string += await RationingString();
    }
    else if (map[0] == 'StrengthToolTip') {
      string += await StrengthString();
    } else {
        string += await hoverString(map[3]);  
    }
    cost.innerHTML = string;
}

async function getBuilding(user_id) {
  currUserName = getCookie('userID').split('userID=')[1]
  try {
      const response = await fetch(backendpath + `/buildings/${user_id}/${currUserName}`); 
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

async function RationingString() {
 string = '';
 string += '<div class="flexitem" style="text-align: left; width: 100%">'
 string += 'You can ration food to make it last longer</div>'
 string += '<div class="flexitem ToolTipLine" width="80%" size="4"></div>' // line
 string += '<div class="flexitem" style="text-align: left; width: 100%">'
 string += 'Health = Rationing*Other Stuff</div>';
 return string;
}

async function StrengthString() {
  return '<div class="flexitem" style="text-align: left; width: 100%">Health effects your strength.</div>' +  '<div class="flexitem" style="text-align: left; width: 100%">Strength = 0.5 + 0.5*Health</div>'

}

async function hoverString(type) {
  currUserName = getCookie('userID').split('userID=')[1]
  try {
    const response = await fetch(backendpath + `/hoverString/${type}/${currUserName}`);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    return data['string'];
  } catch (error) {
    console.error('There was a problem with your fetch operation:', error);
    throw error;
}
}