
// async function getBuilding(user_id) {
//     currUserName = getCookie('userID').split('userID=')[1]

//     try {
//         const response = await fetch(backendpath + `/buildings/${user_id}/${currUserName}`); 
//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error('There was a problem with your fetch operation:', error);
//         throw error;
//     }
//   }