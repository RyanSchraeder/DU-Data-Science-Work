// from data.js
var tableData = data;
var buttonFilter = d3.select("#filter-btn");
var table = d3.select("tbody");  
var inputState = d3.select("#state");
var inputCountry = d3.select("#country");
var inputShape = d3.select("#shape"); 
var inputDate = d3.select("#datetime"); 
var inputCity = d3.select("#city");

// Loop through data objects
tableData.forEach(function(sighting) {
    console.log(sighting) 
}); 

// Append data to table 
tableData.forEach((sighting) => {
    var row = table.append("tr");
    Object.entries(sighting).forEach(([key, value]) => {
        var cell = row.append("td");
        cell.text(value);
    });
});

//On Button click, filter input 
//buttonFilter.on("click",