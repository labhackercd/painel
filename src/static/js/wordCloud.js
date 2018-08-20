Highcharts.seriesTypes.wordcloud.prototype.deriveFontSize = function (relativeWeight) {
   var maxFontSize = 14;
  // Will return a fontSize between 10px and 35px.
  return Math.floor(maxFontSize * relativeWeight) + 6;
};

function selectPoint(point) {
  $('.js-cloud-info-title').text(point.name);

  var tweets = $('.js-cloud-tweets');
  tweets.html('');
  var TweetsData = point.tweets

  hideLoader('cloud-tweets-loader');
  $.each(TweetsData, function(i, d) {
    var element = createTweetCard(d, 'cloud');
    tweets.append(element);
  })
}

function loadWordCloud(params) {
  showLoader('wordcloud-loader');
  showLoader('cloud-tweets-loader');
  $.getJSON('/wordcloud' + params, function(data) {
    hideLoader('wordcloud-loader');
    hideLoader('cloud-tweets-loader');
    var noData = `
      <div class="no-data">
        <div class="icon"></div>
        <h3 class="text-muted">Não encontramos nada</h3>
      </div>
      `;
    $('.js-cloud-tweets').html(noData);
    if ( data.length == 0 ) {
      $("#wordcloud-container").html(noData);
      $('.js-cloud-info-title').text('');
    }
    else {
      $( "#wordcloud-container" ).html('')
      Highcharts.chart('wordcloud-container', {
        plotOptions: {
          series: {
            turboThreshold: 0,
            cursor: 'pointer',
            point: {
              events: {
                click: function (e) {
                  $('.js-wordcloud-text').addClass('-unselected');
                  $(e.target).removeClass('-unselected');
                  selectPoint(this);
                  localStorage.setItem('word', this.name);
                  loadContainers();
                  addFilterTag('pink', 'word', this.name);
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
              $('.js-wordcloud-text').bind('mousedown', function() {
                showLoader('cloud-tweets-loader');
              })
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
          name: 'Ocorrências'
        }],
        title: {
          text: ''
        }
      });
    }
  });
};
