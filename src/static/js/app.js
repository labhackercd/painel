function showLoader(loaderId) {
  $('#' + loaderId).addClass('-show');
}

function hideLoader(loaderId) {
  $('#' + loaderId).removeClass('-show');
}

function compareProfiles(a, b) {
  if (a.tweets_count < b.a.tweets_count) {
    return -1;
  }

  if (a.tweets_count > b.a.tweets_count) {
    return 1;
  }
  return 0;
}

function profileHandleClick(e) {
  var sectionName = e.data.sectionName;
  var tweets = $('.js-' + sectionName + '-tweets');
  tweets.html('');

  var back = $('<h3 class="card-title mb-1 tweets-back"><a class="text-gray" href="">Voltar</a></h3>');
  back.click(function() {
    showInfoContainerProfiles(sectionName);
    $(this).remove();
    return false;
  });

  $('.js-' + sectionName + '-header').append(back);

  $.each(e.data.tweets, function(i, d) {
    tweets.append(createTweetCard(d));
  })

  showInfoContainerTweets(sectionName);

  return false;
}


Highcharts.seriesTypes.wordcloud.prototype.deriveFontSize = function (relativeWeight) {
   var maxFontSize = 25;
  // Will return a fontSize between 10px and 35px.
  return Math.floor(maxFontSize * relativeWeight) + 10;
};

showLoader('wordcloud-loader');
var url = new URL(window.location.href);
var param = '?' + url.searchParams.toString();

$.getJSON('/wordcloud' + param, function(data) {
  hideLoader('wordcloud-loader');
  if ( data.length == 0 ) {
    var html = `
    <div class="no-data">
      <div class="icon"></div>
      <h3 class="text-muted">Não encontramos nada</h3>
    </div>
    `;

    $( ".wordcloud-section .card" ).html(html);
  }
  else {
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

$.getJSON('/static/top-profiles.json', function(data) {
  var topProfiles = $('.js-top-profiles');

  $.each(data, function(i, d) {
    var element = createProfileCard(d, 'top');
    element.click({tweets: d.tweets, sectionName: 'top'}, profileHandleClick);
    topProfiles.append(element);
  })

  showInfoContainerProfiles('top');
});

// Concatenação de filtros na URL e atualização de labels.
// var url foi setada antes do $.getJSON do worldcloud
var category_id = url.searchParams.get("category_id");
var title_date = url.searchParams.get("show_by");

$('.js-category').click(function (e) {
  var categoryId = $(e.target).data('categoryId');
  if (categoryId === 0) {
    url.searchParams.delete('category_id');
  }
  else {
    url.searchParams.set('category_id', categoryId);
  }
  window.location = url;
});

// pegar url atual, ver se tem parametros, se tiver add

$('.js-filter-buttons button').click(function() {
  if ($(this).hasClass('-day')) {
    url.searchParams.delete('show_by')
  } else if ($(this).hasClass('-week')) {
    url.searchParams.set('show_by', 'week')
  } else if ($(this).hasClass('-month')) {
    url.searchParams.set('show_by', 'month')
  }
  window.location = url;
});

var offset = parseInt(url.searchParams.get('offset'));

if (!offset || offset === 0) {
  $('.js-offset-next').addClass('-disabled');
} else {
  $('.js-offset-next').click(function() {
    if (offset === 1) {
      url.searchParams.delete('offset');
    } else {
      url.searchParams.set('offset', offset - 1);
    }

    window.location = url;
  })
}

$('.js-offset-prev').click(function() {
  if (offset) {
    url.searchParams.set('offset', offset + 1);
  } else {
    url.searchParams.set('offset', 1);
  }

  window.location = url;
})
