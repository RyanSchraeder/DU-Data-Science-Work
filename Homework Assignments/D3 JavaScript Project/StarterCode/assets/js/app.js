console.log(' Within app.js asset file')

var svgWidth = 1000; 
var svgHeight = 500;

    //Create SVG element
var svg = d3.select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

    //Load CSV
d3.csv('../assets/data/data.csv', function(error, newsData) {
    if (error) return console.warn(error);
    console.log(newsData);

});
