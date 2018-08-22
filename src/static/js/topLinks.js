function loadTopLinks(params) {
  var linksRequest = $.ajax({
    dataType: "json",
    url: '/top-links',
    data: params,
    beforeSend : function() {
      showLoader('top-links-loader');
      if(linksRequest != null) {
        linksRequest.abort();
      }
    },
  }).done(function(data) {
    var topLinks = $('.js-top-links');
    topLinks.html('');
    if (data.length) {
      $.each(data, function(i, data) {
        if (data.title) {
          var title = data.title;
        } else {
          var title = '';
        }

        var element = `
          <div class="item">
            <div class="bar js-top-link-bar">
              <div class="content">
                <h2>${title}</h2>
                <a class="js-top-link-href" href="${data.url}" target="_blank">${data.display_url}</a>
              </div>
              <div class="mentions">
                <span class="value">${data.retweets}</span>
                <span>menções</span>
              </div>
            </div>
          </div>
        `
        var element = $(element)
        element.on('click', '.js-top-link-href', function(e) {
          window.open($(this).attr('href'), '_blank');
        });
        element.on('click', '.js-top-link-bar', {link: data.id, url: data.display_url}, function(e) {
          localStorage.setItem('link', e.data['link']);
          addFilterTag('blue', 'link', e.data['url']);
          loadContainers();

          return false;
        });
        topLinks.append(element);
      })
    } else {
      topLinks.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }

    hideLoader('top-links-loader');
  });
};
