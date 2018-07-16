Highcharts.seriesTypes.wordcloud.prototype.deriveFontSize = function (relativeWeight) {
   var maxFontSize = 25;
  // Will return a fontSize between 5px and 30px.
  return Math.floor(maxFontSize * relativeWeight) + 5;
};

$.getJSON('/wordcloud', function(data) {
  Highcharts.chart('wordcloud-container', {
      plotOptions: {
          series: {
              cursor: 'pointer',
              point: {
                  events: {
                      click: function () {
                          console.log(this)
                      }
                  }
              }
          }
      },

    series: [{
      type: 'wordcloud',
      spiral: 'rectangular',
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