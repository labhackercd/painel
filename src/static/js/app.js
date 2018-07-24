function showLoader(loaderId) {
  $('#' + loaderId).addClass('-show');
}

function hideLoader(loaderId) {
  $('#' + loaderId).removeClass('-show');
}

function showProfile() {
  var profiles = $('.js-cloud-profiles');
  var tweets = $('.js-cloud-tweets');
  profiles.removeClass('-hide');
  tweets.addClass('-hide');
  $('.card-cloud-profiles').animate({ scrollTop: 0 }, 250);
}

function showTweets() {
  var profiles = $('.js-cloud-profiles');
  var tweets = $('.js-cloud-tweets');
  profiles.addClass('-hide');
  tweets.removeClass('-hide');
  $('.card-cloud-profiles').animate({ scrollTop: 0 }, 250);
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

function createTweetCard(data) {
  var html = `
  <div class="row ticket-card mt-3 pb-2 border-bottom pb-3 mb-3" >
    <div class="col-md-1">
      <img class="img-sm rounded-circle mb-4 mb-md-0" src="${data.profile.image_url}" alt="profile image">
    </div>
    <div class="ticket-details col-md-9">
      <div class="d-flex">
        <p class="text-dark font-weight-semibold mr-2 mb-0 no-wrap">${data.profile.name}</p>
        <p class="text-primary mr-1 mb-0"><a class="text-gray" href="https://twitter.com/${data.profile.screen_name}">@${data.profile.screen_name}</a></p>
      </div>
      <p class="text-gray mb-2">
        ${data.text}
      </p>
      <div class="row text-gray">
        <div class="col d-flex">
          <p class="mr-2"><i class="mdi mdi-twitter-retweet"></i>${data.retweet_count}</p>
          <p><i class="mdi mdi-heart"></i>${data.favorite_count}</p>
        </div>
      </div>
    </div>
  </div>
  `;

  return $(html);
}

function createProfileCard(data) {
  var html = `
  <div class="row ticket-card mt-3 pb-2 border-bottom pb-3 mb-3 js-cloud-profile" data-tweets="${data.tweets_count}">
    <div class="col-md-1">
      <img class="img-sm rounded-circle mb-4 mb-md-0" src="${data.image_url}" alt="profile image">
    </div>
    <div class="ticket-details col-md-9">
      <div class="d-flex">
        <p class="text-dark font-weight-semibold mr-2 mb-0 no-wrap">${data.name}</p>
        <p class="text-primary mr-1 mb-0"><a class="text-gray" href="https://twitter.com/${data.screen_name}">@${data.screen_name}</a></p>
      </div>
      <p class="text-gray ellipsis mb-2">
        <span class="font-weight-bold">${data.followers_count}</span> seguidores
      </p>
      <div class="row text-gray">
        <div class="col d-flex">
          <small class="text-muted"><a href="">Ver ${data.tweets_count} tweets sobre o tema</a></small>
        </div>
      </div>
    </div>
  </div>
  `;

  return $(html);
}

function showProfileTweets(e) {
  var tweets = $('.js-cloud-tweets');
  tweets.html('');

  var back = $('<h3 class="card-title mb-1 tweets-back js-tweets-back"><a class="text-gray" href="">Voltar</a></h3>');
  back.click(function() {
    showProfile();
    return false;
  });

  tweets.append(back);

  $.each(e.data.tweets, function(i, d) {
    tweets.append(createTweetCard(d));
  })

  showTweets();

  return false;
}


Highcharts.seriesTypes.wordcloud.prototype.deriveFontSize = function (relativeWeight) {
   var maxFontSize = 25;
  // Will return a fontSize between 10px and 35px.
  return Math.floor(maxFontSize * relativeWeight) + 10;
};

showLoader('wordcloud-loader');
var url = new URL(window.location.href);
var category_id = url.searchParams.get("category_id");
var param = ''
if (category_id){
  param = '?category_id=' + category_id
}

$.getJSON('/wordcloud' + param, function(data) {
  hideLoader('wordcloud-loader');
  Highcharts.chart('wordcloud-container', {
    plotOptions: {
      series: {
        cursor: 'pointer',
        point: {
          events: {
            click: function (e) {
              $('.js-wordcloud-text').addClass('-unselected');
              $(e.target).removeClass('-unselected');

              $('.js-cloud-title').text(this.name);

              var profiles = $('.js-cloud-profiles');
              profiles.html('');
              var profilesData = this.profiles

              var sortedProfiles = Object.keys(this.profiles).sort(function(a, b) {
                return profilesData[b].tweets_count - profilesData[a].tweets_count;
              })

              $.each(sortedProfiles, function(i, d) {
                var data = profilesData[d];

                var element = createProfileCard(data);
                element.click({tweets: data.tweets}, showProfileTweets);
                profiles.append(element);
              })

              showProfile();
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
})
