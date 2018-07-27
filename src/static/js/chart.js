function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

var url = new URL(window.location.href);
var param = '?' + url.searchParams.toString();

$('#chart-loader').addClass('-show');

$.getJSON('/areachart' + param, function(data) {  
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

  $('#chart-loader').removeClass('-show');

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

  var title_date = 'Hoje'
  var title_chart = data.labels[data.labels.length-1]
  
  if (url.searchParams.get("show_by")) {
    title_date = data.labels[data.labels.length-1]
  }

  $(".chart-title").text(title_chart);
  $('.js-title-date').text(title_date);
});
