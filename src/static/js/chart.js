function loadChart(params) {
  var colors = () => randomColor({
     luminosity: 'dark',
     format: 'rgba',
     alpha: 0.4
  });

  showLoader('chart-loader');

  $.getJSON('/areachart' + params, function(data) {
    $('.chart-title').text(data.page_title);
    $('.js-title-date').text(data.page_title);
    $('.js-tweets-count').text(data.tweets_count);
    $('.js-profiles-count').text(data.profiles_count);

    if (typeof data.variation == 'number') {
      if (data.variation > 0) {
        $('.js-variation').html(`
          ${data.variation.toFixed(2)}% <i class="text-success mdi mdi-arrow-up"></i>
        `);
      } else if (data.variation < 0) {
        $('.js-variation').html(`
          ${data.variation.toFixed(2)}% <i class="text-danger mdi mdi-arrow-down"></i>
        `);
      } else {
        $('.js-variation').html(`
          ${data.variation}%
        `);
      }
    } else {
      $('.js-variation').html(`
        <i class="fas fa-infinity"></i> %
        <i class="text-success mdi mdi-arrow-up"></i>
      `);
    }
  }).done(function(response) {
    chart.destroy();
    var datasets = new Array();
    $.each(response.categories, function(key, value){
      var color = colors();
      datasets.push({
        label: key,
        data: value,
        borderColor: color,
        pointBackgroundColor: color,
        pointRadius: 5,
        pointHoverBorderWidth: 7,
        borderWidth: 2,
        fill: true,
        backgroundColor: color,
      });
    });

    var areaData = {
      labels: response.labels,
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

    hideLoader('chart-loader');

    chart = new Chart(areaChartCanvas, {
      type: 'line',
      data: areaData,
      options: areaOptions
    });
  });
};
