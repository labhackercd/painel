function createTweetCard(data) {
  var html = `
  <div class="row ticket-card mt-3 pb-2 border-bottom pb-3 mb-3" >
    <div class="col-md-1">
      <img class="img-sm rounded-circle mb-4 mb-md-0" src="${data.profile.image_url}" alt="profile image">
    </div>
    <div class="ticket-details col-md-9">
      <div class="d-flex">
        <p class="text-dark font-weight-semibold mr-2 mb-0 no-wrap">${data.profile.name}`
        + ( data.profile.verified ? '<i class="twitter-verify"></i>' : '')
        +`</p>
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

function createProfileCard(data, sectionName) {
  var html = `
  <div class="row ticket-card mt-3 pb-2 border-bottom pb-3 mb-3 js-${sectionName}-profile" data-tweets="${data.tweets_count}">
    <div class="col-md-1">
      <img class="img-sm rounded-circle mb-4 mb-md-0" src="${data.image_url}" alt="profile image">
    </div>
    <div class="ticket-details col-md-9">
      <div class="d-flex">
        <p class="text-dark font-weight-semibold mr-2 mb-0 no-wrap">${data.name}`
        + ( data.verified ? '<i class="twitter-verify"></i>' : '')
        +`</p>
        <p class="text-primary mr-1 mb-0"><a class="text-gray" href="https://twitter.com/${data.screen_name}">@${data.screen_name}</a></p>
      </div>
      <p class="text-gray ellipsis mb-2">
        <span class="font-weight-bold">${data.followers_count}</span> seguidores
      </p>
      <div class="row text-gray statistics">
        <div class="col d-flex">
          <p class="mr-2"><i class="mdi mdi-twitter-retweet"></i>${data.retweet_count}</p>
          <p><i class="mdi mdi-heart"></i>${data.favorite_count}</p>
        </div>
      </div>
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


function showInfoContainerProfiles(sectionName) {
  var profiles = $('.js-' + sectionName + '-profiles');
  var tweets = $('.js-' + sectionName + '-tweets');
  profiles.removeClass('-hide');
  tweets.addClass('-hide');
  profiles.closest('.js-cloud-wrapper').animate({ scrollTop: 0 }, 250);
}

function showInfoContainerTweets(sectionName) {
  var profiles = $('.js-' + sectionName + '-profiles');
  var tweets = $('.js-' + sectionName + '-tweets');
  profiles.addClass('-hide');
  tweets.removeClass('-hide');
  profiles.closest('.js-cloud-wrapper').animate({ scrollTop: 0 }, 250);
}
