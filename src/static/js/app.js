function showLoader(loaderId) {
  $('#' + loaderId).addClass('-show');
}

function hideLoader(loaderId) {
  $('#' + loaderId).removeClass('-show');
}

Highcharts.seriesTypes.wordcloud.prototype.deriveFontSize = function (relativeWeight) {
   var maxFontSize = 25;
  // Will return a fontSize between 5px and 30px.
  return Math.floor(maxFontSize * relativeWeight) + 10;
};

showLoader('wordcloud-loader');
$.getJSON('/wordcloud', function(data) {
  hideLoader('wordcloud-loader');
  Highcharts.chart('wordcloud-container', {
      plotOptions: {
          series: {
              cursor: 'pointer',
              point: {
                  events: {
                      click: function (e) {
                          console.log(this)
                          $('.js-wordcloud-text').addClass('-unselected');
                          $(e.target).removeClass('-unselected');

                      }
                  }
              }
          }
      },

    chart: {
      events: {
        load: function() {
          var points = this.series[0].points;

          points.forEach(function(p, i) {
            p.update({
              className: 'js-wordcloud-text wordcloud-text'
            }, false);
          })
          this.redraw();

        }
      }
    },

    series: [{
      type: 'wordcloud',
      spiral: 'rectangular',
      className: 'js-wordcloud',
      placementStrategy: 'center',
      rotation: {
        from: 0,
        to: 0
      },
      data: data,
      name: 'Occurrences'
    }],
    title: {
      text: ''
    }
  });
})