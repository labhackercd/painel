function loadChart() {
  var colors = () => randomColor({
     luminosity: 'dark',
     format: 'rgba',
     alpha: 1
  });

  var param = '?';
  if(localStorage.getItem('show_by') != null){
    param += 'show_by=' + localStorage.getItem('show_by') + '&';
  }
  if(localStorage.getItem('category_id') != null){
    param += 'category_id=' + localStorage.getItem('category_id') + '&';
  }
  if(localStorage.getItem('offset') != null){
    param += 'offset=' + localStorage.getItem('offset');
  }

  showLoader('chart-loader');

  $.getJSON('/areachart' + param, function(data) {
    var datasets = new Array();
    $.each(data.categories, function(key, value){
      var color = colors();
      datasets.push({
        label: key,
        data: value,
        borderColor: color,
        pointBackgroundColor: color,
        pointRadius: 5,
        pointHoverBorderWidth: 7,
        borderWidth: 2,
        fill: false,
        backgroundColor: color,
      });
    });

    hideLoader('chart-loader');

    var areaData = {
      labels: data.labels,
      datasets: datasets,
    };

    var areaOptions = {
      responsive: true,
  	  maintainAspectRatio: true,
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
      scales: {
    		xAxes: [{
    			gridLines: {
    				lineWidth: 1
    			},
          ticks: {
            fontSize: 14,
            padding: 10,
            labelString: 'tweets'
          },
    		}],
    		yAxes: [{
    			gridLines: {
    				lineWidth: 1
    			},
          ticks: {
            fontSize: 14,
            padding: 10,
            labelString: 'tweets'
          },
    		}],
    	},
      tooltips: {
    		xPadding: 10,
    		yPadding: 10,
        titleMarginBottom: 12,
        displayColors: false,
        titleFontSize: 16,
        bodyFontSize: 14,
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

    $(".chart-title").text(data.page_title);
    $('.js-title-date').text(data.page_title);
  });
};