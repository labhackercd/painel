var url = new URL(window.location.href);
var param = '?' + url.searchParams.toString();

$('#top-publications-loader').addClass('-show');
$.getJSON('/top-tweets' + param, function(data) {
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
  $('#top-publications-loader').removeClass('-show');
});