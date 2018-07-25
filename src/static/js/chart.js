function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

$.getJSON('/areachart', function(data) {
  var datasets = new Array();
  $.each(data.categories, function(key, value){ 
    datasets.push({
      label: key,
      data: value,
      borderColor: getRandomColor(),
      borderWidth: 1,
      fill: false,
    });
  });

  var areaData = {
    labels: data.labels,
    datasets: datasets,
  };

  var areaOptions = {
    plugins: {
      filler: {
        propagate: true
      }
    }
  }

  // Get context with jQuery - using jQuery's .get() method.
  if ($("#areaChart").length) {
    var areaChartCanvas = $("#areaChart").get(0).getContext("2d");
    var areaChart = new Chart(areaChartCanvas, {
      type: 'line',
      data: areaData,
      options: areaOptions
    });
  }
});
