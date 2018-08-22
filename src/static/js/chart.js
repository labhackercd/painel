var chartRequest = null;
function loadChart(params) {
  var colors = () => randomColor({
     luminosity: 'light',
     format: 'rgba',
     alpha: 1
  });

  chartRequest = $.ajax({
    dataType: "json",
    url: '/areachart',
    data: params,
    beforeSend : function() {
      showLoader('chart-loader');
      if(chartRequest != null) {
        chartRequest.abort();
      }
    },
  }).done(function(data) {
    var title = $('.js-title-date').get(0);
    var text_to_change = title.childNodes[0];
    text_to_change.nodeValue = data.page_title;

    $('.chart-title').text(data.page_title);
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

    chart.destroy();
    var datasets = new Array();
    $.each(data.categories, function(key, value){
      var color = colors();
      datasets.push({
        label: key,
        data: value.values,
        borderColor: value.color,
        pointBackgroundColor: value.color,
        pointRadius: 5,
        pointHoverBorderWidth: 7,
        borderWidth: 2,
        fill: false,
        backgroundColor: value.color
      });
    });

    var areaData = {
      labels: data.labels,
      datasets: datasets
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
          padding: 20,
          fullWidht: true,
          fontColor: '#FFF'
        },
      },
      scales: {
        xAxes: [{
          stacked: true,
          gridLines: {
            lineWidth: 1,
            color: 'rgba(255, 255, 255, 0)',
            zeroLineColor: 'rgba(255, 255, 255, 0)'
          },
          ticks: {
            fontSize: 10,
            padding: 10,
            fontColor: '#FFF'
          },
        }],
        yAxes: [{
          gridLines: {
            lineWidth: 1,
            color: 'rgba(255, 255, 255, 0.05)',
            zeroLineColor: 'rgba(255, 255, 255, 0)'
          },
          ticks: {
            display: false,
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
    chartRequest = null;

    chart = new Chart(areaChartCanvas, {
      type: 'line',
      data: areaData,
      options: areaOptions
    });
  });
};
