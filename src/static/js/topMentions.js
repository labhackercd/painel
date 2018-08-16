function loadTopMentions(params) {
  showLoader('top-mentions-loader');
  $.getJSON('/top-mentions' + params, function(data) {
    var topMentions = $('.js-top-mentions');
    topMentions.html('');
    if (data.length) {
      var max_engagement = data[0].engagement
      $.each(data, function(i, data) {
        var element = `
          <div class="item">
            <span>${data.screen_name}</span>
            <img src="https://avatars.io/twitter/${data.screen_name}" alt="profile image">
            <span class="value">${data.retweets}</span>
            <span>Tweets</span>
          </div>
        `
        var element = $(element)
        element.click({mentioned_id: data.id}, function(e) {
          localStorage.setItem('mentioned_id', e.data['mentioned_id']);
          loadContainers();

          return false;
        });
        topMentions.append(element);
      })
    } else {
      topMentions.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }

    hideLoader('top-mentions-loader');
  });
};
