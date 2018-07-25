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
    var color = getRandomColor();
    datasets.push({
      label: key,
      data: value,
      borderColor: color,
      pointBackgroundColor: color,
      borderWidth: 2,
      fill: false,
      backgroundColor: color,
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
    },
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 30,
        fullWidht: true,
      },
    },
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
