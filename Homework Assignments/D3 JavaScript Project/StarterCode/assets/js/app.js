var svgWidth = 860;
var svgHeight = 500;

var margin = {
    top: 30,
    right: 50,
    bottom: 60,
    left: 50
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);


d3.csv("../assets/data/data.csv")
    .then(function (usData) {
        usData.forEach(function (data) {
            data.poverty = +data.poverty;
            data.healthcare = +data.healthcare;
        })

        var xLinearScale = d3.scaleLinear()
            .domain([0, d3.max(usData, d => d.poverty)])
            .range([0, width])


        console.log(xLinearScale)

        var yLinearScale = d3.scaleLinear()
            .domain([0, d3.max(usData, d => d.healthcare)])
            .range([height, 3]);

        var bottomAxis = d3.axisBottom(xLinearScale);
        var leftAxis = d3.axisLeft(yLinearScale);

        chartGroup.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(bottomAxis);

        chartGroup.append("g")
            .call(leftAxis);

        var circlesGroup = chartGroup.selectAll("circle")
            .data(usData)
            .enter()
            .append("circle")
            .attr("cx", d => xLinearScale(d.poverty))
            .attr("cy", d => yLinearScale(d.healthcare))
            .attr("r", "10")
            .attr("fill", "blue")
            .attr("opacity", 9.0)
    });