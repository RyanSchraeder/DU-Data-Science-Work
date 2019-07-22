console.log('Within app.js asset file')

var svgWidth = 1000; 
var svgHeight = 500;

    //Create SVG element
var svg = d3.select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);


    //Set chart margins even
var chartHeight = svgHeight - margin.top - margin.bottom;
var chartWidth = svgWidth - margin.left - margin.right;

// create svg container and shift everything over by the margins using transform/translate.
var svg = d3
    .select('#scatter')
    .append('svg')
    .attr('width', svgWidth)
    .attr('height', svgHeight)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

var chartGroup = svg.append("g")

    //Load CSV
d3.csv('../assets/data/data.csv', function (error, newsData) {
        if (error) return console.warn(error);
        console.log(newsData);

    //process csv file using a for loop.
    for (var i = 0; i < newsData.length; i++) {
        console.log(i, newsData[i].state, newsData[i].poverty, newsData[i].healthcare);
        console.log(i, newsData[i].obesity, newsData[i].income);
    }

    newsData.forEach(function (data) {
        data.poverty = +data.poverty;
        data.healthcare = +data.healthcare;
    })

    // Create scale functions. scale y to chart height.
    var yLinearScale = d3.scaleLinear().range([chartHeight, 0]);
    // scale x to chart width.
    var xLinearScale = d3.scaleLinear().range([0, chartWidth]);

    // Create axis functions
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    // Scale the domain
    xLinearScale.domain([8,
        d3.max(newsData, function (data) {
            return +data.poverty * 1.05;
        }),
    ]);

    yLinearScale.domain([0,
        d3.max(newsData, function (data) {
            return +data.healthcare * 1.1;
        }),
    ]);

    console.log("creating tooltip")
    // Create tool tip
    var toolTip = d3
        .tip()
        .attr('class', 'tooltip')
        .offset([60, 15])
        //.offset([80, -60])
        .html(function (data) {
            var state = data.state;
            var poverty = +data.poverty;
            var healthcare = +data.healthcare;
            return (
                state + '<br> Poverty Percentage: ' + poverty + '<br> Lacks Healthcare Percentage: ' + healthcare
            );
        });

    chartGroup.call(toolTip);

    // Generate Scatter Plot
    chartGroup
        .selectAll('circle')
        .data(newsData)
        .enter()
        .append('circle')
        .attr('cx', function (data, index) {
            return xLinearScale(data.poverty);
        })
        .attr('cy', function (data, index) {
            return yLinearScale(data.healthcare);
        })
        .attr('r', '16')
        .attr('fill', 'lightgreen')
        .attr('fill-opacity', 0.6)
        //.on('click', function(data) {
        // Display tooltip on mouseover. 
        .on("mouseover", function (data) {
            toolTip.show(data);
        })
        // Hide and Show on mouseout
        .on("mouseout", function (data, index) {
            toolTip.hide(data);
        });

    chartGroup
        .append('g')
        .attr('transform', `translate(0, ${chartHeight})`)
        .call(bottomAxis);

    chartGroup.append('g').call(leftAxis);

    svg.selectAll(".dot")
        .data(newsData)
        .enter()
        .append("text")
        .text(function (data) { return data.abbr; })
        .attr('x', function (data) {
            return xLinearScale(data.poverty);
        })
        .attr('y', function (data) {
            return yLinearScale(data.healthcare);
        })
        .attr("font-size", "10px")
        .attr("fill", "black")
        .style("text-anchor", "middle");

    chartGroup
        .append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left + 40)
        .attr('x', 0 - chartHeight / 2)
        .attr('dy', '1em')
        .attr('class', 'axisText')
        .text('No Healthcare (%)');

    // x-axis labels
    chartGroup
        .append('text')
        .attr(
            'transform',
            'translate(' + chartWidth / 2 + ' ,' + (chartHeight + margin.top + 40) + ')',
        )
        .attr('class', 'axisText')
        .text('Poverty (%)');

    //Need to add event listeners with transitions for obesity vs income. 

});
