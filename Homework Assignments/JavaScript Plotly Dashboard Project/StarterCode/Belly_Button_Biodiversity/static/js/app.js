var selector;
var selector_data = []
// var bubble_trace = [];

function buildMetadata(sample) {
  console.log("buildMetadata");

  // @TODO: Complete the following function that builds the metadata panel

  d3.json(`/metadata/${sample}`).then((data) => {

    // Use d3 to select the panel with id of `#sample-metadata`

    console.log(data);
    console.log("==========")

    var metadataPanel = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata

    metadataPanel.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.

    Object.entries(data).forEach(([key, value]) => {
      metadataPanel.append("h6").text(`${key}: ${value}`);
    });
  });
}

// function buildSampleData(sample) {
//   console.log("buildSampleData");

//   d3.json(`/samples/${sample}`).then((data) => {
//     console.log(data);
//     console.log("==========")

//     selector_data.push(data);
//     console.log("Selector Data: ", selector_data)

//     selector_data[0].otu_ids.forEach(function (index, item) {
//       console.log("otu_id: ", item)

//       bubble_trace.push({
//         x: item
//       })

//     })

//     selector_data[0].sample_values.forEach(function (index, item) {
//       console.log("sample_values: ", item)

//       if(bubble_trace[index]) {
//         bubble_trace[index].y = item;
//       }

//     })

//     selector_data[0].otu_labels.forEach(function (index, item) {
//       console.log("otu_label: ", item)
//     })

//     console.log("bubble:  ", bubble_trace);

//   });
// };

// BONUS: Build the Gauge Chart
//  buildGauge(data.WFREQ);

// @TODO: Use `d3.json` to fetch the sample data for the plots

// First, build your trace and initialize data selection with path. 
// Then, customize the pie with title, radius, color, text size, cursor hover response

// HINT: You will need to use slice() to grab the top 10 sample_values,
// otu_ids, and labels (10 each).

function buildCharts(sample) {
  console.log("buildCharts");
  d3.json(`/samples/${sample}`).then((data) => {
    
    console.log(data); 

    const otu_ids = data.otu_ids;
    const otu_labels = data.otu_labels;
    const sample_values = data.sample_values;

    console.log(otu_ids, otu_labels, sample_values)

    // Build a Bubble Chart

    var bubbleLayout = {
      margin: { t: 0 },
      hovermode: "closest",

      xaxis: { title: "OTU ID" }
    };
    var bubbleData = [
      {
        x: otu_ids,
        y: sample_values,
        text: otu_labels,
        mode: "markers",
        marker: {
          size: sample_values,
          color: otu_ids,
          colorscale: "Earth"
        }
      }
    ];
    console.log(bubbleData); 

    Plotly.plot("bubble", bubbleData, bubbleLayout);

    // @TODO: Build a Pie Chart

    var pieData = [
      {
        values: sample_values.slice(0, 10),
        labels: otu_ids.slice(0, 10),
        hovertext: otu_labels.slice(0, 10),
        hoverinfo: "hovertext",
        hovermode: "closest",
        type: "pie"
      }
    ];

    var pieLayout = {
      margin: { t: 0, l: 0 }
    };
    console.log(bubbleData);

    Plotly.plot("pie", pieData, pieLayout);
  });
}

function init() {

  // Grab a reference to the dropdown select element

  selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options

  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots

    const firstSample = sampleNames[0];

    console.log("firstSample", firstSample);

    buildCharts(firstSample);

    buildMetadata(firstSample);

  });
}

function optionChanged(newSample) {

  // Fetch new data each time a new sample is selected

  console.log(newSample);
  buildCharts(newSample);
  buildMetadata(newSample);
  // buildSampleData(newSample);
  // bubble_trace(newSample);
}

// Initialize the dashboard
init();
console.log("initializing"); 