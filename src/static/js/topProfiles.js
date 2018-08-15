function loadTopProfiles(params) {
  showLoader('main-influencers-loader');
  $.getJSON('/top-profiles' + params, function(data) {
    var topProfiles = $('.js-top-profiles');
    topProfiles.html('');
    if (data.length) {
      var max_engagement = data[0].engagement
      $.each(data, function(i, d) {
        var element = createProfileCard(d, max_engagement);
        element.click({profile_id: d.id}, profileHandleClick);
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

    hideLoader('main-influencers-loader');
  });
};
