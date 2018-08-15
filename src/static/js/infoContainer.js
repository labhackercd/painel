function createTweetCard(data) {
  var categories = "";
  $.each(data.categories, function (index, element){
    categories += `<button type="button" class="btn btn-inverse-secondary btn-rounded btn-fw">${element}</button>`
  });

  var html = `
  <div class="item">
    <div class="avatar">
      <img src="${data.profile.image_url}" alt="profile image">
    </div>
    <div class="content">
      <div class="header">
        <h3>${data.profile.name}`
        + ( data.profile.verified ? '<i class="twitter-verify"></i>' : '')
        +`</h3>
        <a href="https://twitter.com/${data.profile.screen_name}">@${data.profile.screen_name}</a>
      </div>
      <div class="info">
        <p>${data.text}</p>
        <div class="section-statistics">
          <span><i class="mdi mdi-twitter-retweet"></i>${data.retweet_count}</span>
          <span><i class="mdi mdi-heart"></i>${data.favorite_count}</span>
        </div>
        <div class="category-flag">
          ${categories}
        </div>
      </div>
    </div>
  </div>
  `;

  return $(html);
}

function createProfileCard(data, sectionName) {
  var html = `
  <div class="item js-${sectionName}-profile" data-profile-id="${data.id}" data-tweets="${data.tweets_count}">
    <div class="avatar">
      <img src="${data.image_url}" alt="profile image">
    </div>
    <div class="content">
      <div class="header">
        <h3>${data.name}`
        + ( data.verified ? '<i class="twitter-verify"></i>' : '')
        +`</h3>
        <a href="https://twitter.com/${data.screen_name}">@${data.screen_name}</a>
      </div>
      <div class="info">
        <span class="followers">${data.followers_count}</span> seguidores
        <div class="statistics">
          <span><i class="mdi mdi-twitter-retweet"></i>${data.retweet_count}</span>
          <span><i class="mdi mdi-heart"></i>${data.favorite_count}</span>
        </div>
        <a class="read-more" href="">Ver ${data.tweets_count} tweets sobre o tema</a>
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

function profileHandleClick(e) {
  localStorage.setItem('profile_id', e.data['profile_id']);
  loadContainers();

  return false;
}
