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

function createProfileCard(data, max_engagement) {
  var html = `
   <div class="item" data-profile-id="${data.id}">
      <div class="user">
        <img src="${data.image_url}" alt="profile image">
        <h4 class="name">${data.name}</h4>
      </div>
      <div class="bar">
        <progress max="${max_engagement}" value="${data.engagement}"></progress>
        <span class="value">
          <div class="section-statistics">
            <span><i class="mdi mdi-twitter-retweet"></i>${data.retweet_count}</span>
            <span><i class="mdi mdi-heart"></i>${data.favorite_count}</span>
          </div>
        </span>
      </div>
    </div>
  `;

  return $(html);
}

function profileHandleClick(e) {
  localStorage.setItem('profile_id', e.data['profile_id']);
  loadContainers();
  addFilterTag('yellow', 'profile_id', e.data['name']);
  return false;
}
