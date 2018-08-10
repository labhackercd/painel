function compareProfiles(a, b) {
  if (a.tweets_count < b.a.tweets_count) {
    return -1;
  }

  if (a.tweets_count > b.a.tweets_count) {
    return 1;
  }
  return 0;
}

Highcharts.seriesTypes.wordcloud.prototype.deriveFontSize = function (relativeWeight) {
   var maxFontSize = 25;
  // Will return a fontSize between 10px and 35px.
  return Math.floor(maxFontSize * relativeWeight) + 10;
};

function loadWordCloud(params) {
  showLoader('wordcloud-loader');
  $.getJSON('/wordcloud' + params, function(data) {
    hideLoader('wordcloud-loader');
    var noData = `
      <div class="no-data">
        <div class="icon"></div>
        <h3 class="text-muted">Não encontramos nada</h3>
      </div>
      `;
    $('.js-cloud-profiles').html(noData);
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

                  $('.js-cloud-info-title').text(this.name);

                  var profiles = $('.js-cloud-profiles');
                  profiles.html('');
                  var profilesData = this.profiles

                  var sortedProfiles = Object.keys(this.profiles).sort(function(a, b) {
                    return profilesData[b].tweets_count - profilesData[a].tweets_count;
                  })

                  $.each(sortedProfiles, function(i, d) {
                    var data = profilesData[d];

                    var element = createProfileCard(data, 'cloud');
                    element.click({tweets: data.tweets, sectionName: 'cloud'}, profileHandleClick);
                    profiles.append(element);
                  })

                  showInfoContainerProfiles('cloud');
                  hideLoader('cloud-profile-loader');
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

              $('.js-wordcloud-text').bind('mousedown', function() {
                showLoader('cloud-profile-loader');
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
          name: 'Occurrences'
        }],
        title: {
          text: ''
        }
      });
    }
  });
};