function loadTopProfiles(params) {
  showLoader('top-profile-loader');
  $.getJSON('/top-profiles' + params, function(data) {
    var topProfiles = $('.js-top-profiles');
    topProfiles.html('');
    if (data.length) {
      $.each(data, function(i, d) {
        var element = createProfileCard(d, 'top');
        element.click({tweets: d.tweets, sectionName: 'top'}, profileHandleClick);
        topProfiles.append(element);
      })
    } else {
      topProfiles.html(`
          <div class="no-data">
              <div class="icon"></div>
              <h3 class="text-muted">Não encontramos nada</h3>
          </div>
      `)
    }

    showInfoContainerProfiles('top');
    hideLoader('top-profile-loader');
  });
};