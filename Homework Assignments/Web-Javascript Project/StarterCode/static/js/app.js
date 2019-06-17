// from data.js
var tableData = data;
var buttonFilter = d3.select("#filter-btn");
var table = d3.select("tbody");
var inputState = d3.select("#state");
var inputCountry = d3.select("#country");
var inputShape = d3.select("#shape");
var inputDate = d3.select("#datetime");
var inputCity = d3.select("#city");
var dateValue

// Loop through data objects
// tableData.forEach(function(sighting) {
//     console.log(sighting) 
// }); 

console.log(tableData);

// Append data to table 
// tableData.forEach((sighting) => {
//     var row = table.append("tr");
//     Object.entries(sighting).forEach(([key, value]) => {
//         var cell = row.append("td");
//         cell.text(value);
//     });
// });

function insertdata(array) {
    table.html("");
    array.forEach((sighting) => {
        var row = table.append("tr");
        Object.entries(sighting).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });
};

//On Button click, filter input 

buttonFilter.on("click", function () {

    d3.event.preventDefault();

    // Get the value property of the input element
    var dateValue = inputDate.property("value");
    //    var stateValue = inputState.property("value");

    // Prevent the whole page from refreshing.
    console.log(" Input -- Entry ")
    console.log("dateValue  " + dateValue);
    //    console.log("stateValue " + stateValue);
    console.log(" Processing date/value entry ")
    filterData = tableData;

    //    var filterData = tableData.filter(filterData => (filterData.datetime == dateValue) && (filterData.state == stateValue));
    var filterData = tableData.filter(paramData => (paramData.datetime == dateValue));

    console.log(filterData)
    // loadFiltData = "y";
    // if (loadFiltData == 'y') {
    //     console.log("input filter data 'y'")
    //     finalData = filterData;
    // }
    // else {
    //     console.log("input filter data 'n'")
    //     finalData = tableData;
    // }

    //Clear all previous data from UFO table to isolate search results
    //    inputTbody.html("");

    console.log(' Loading Filter Data ');

    insertdata(filterData);
});
console.log(' First time load ');
insertdata(tableData)