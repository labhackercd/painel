function loadTopHashtags(params) {
  showLoader('top-hashtags-loader');
  $.getJSON('/top-hashtags' + params, function(data) {
    var topHashtags = $('.js-top-hashtags');
    topHashtags.html('');
    if (data.length) {
      $.each(data, function(i, data) {
        var element = `
          <div class="item">
            <div class="bar">
              <span class="hashtag">#${data.text}</span>
              <div class="value" style="width: ${data.value}%"></div>
            </div>
          </div>
        `
        var element = $(element)
        element.click({hashtag: data.text}, function(e) {
          localStorage.setItem('hashtag', e.data['hashtag']);
          loadContainers();

          return false;
        });
        topHashtags.append(element);
      })
    } else {
      topHashtags.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }

    hideLoader('top-hashtags-loader');
  });
};
