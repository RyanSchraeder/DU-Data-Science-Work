function buildMetadata(sample) {
  console.log("buildMetadata");
  // @TODO: Complete the following function that builds the metadata panel

  d3.json(`/metadata/${sample}`).then((data) => {
    // Use d3 to select the panel with id of `#sample-metadata`
    console.log(data);

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

    // BONUS: Build the Gauge Chart
    //  buildGauge(data.WFREQ);

  // @TODO: Use `d3.json` to fetch the sample data for the plots

function buildCharts(sample) {
  console.log("buildCharts");

  // @TODO: Build a Bubble Chart using the sample data

  // @TODO: Build a Pie Chart

  // HINT: You will need to use slice() to grab the top 10 sample_values,
  // otu_ids, and labels (10 each).

};

function init() {

  // Grab a reference to the dropdown select element

  var selector = d3.select("#selDataset");

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
}

// Initialize the dashboard
init();
