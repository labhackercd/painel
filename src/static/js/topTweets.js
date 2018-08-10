function loadTopTweets(params) {
  showLoader('top-publications-loader');
  $.getJSON('/top-tweets' + params, function(data) {
    var topTweets = $('.js-top-publications');
    topTweets.html('');
    if (data.length) {
        $.each(data, function(i, d) {
          topTweets.append(createTweetCard(d));
        })
    } else {
      topTweets.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }
    hideLoader('top-publications-loader');
  });
};