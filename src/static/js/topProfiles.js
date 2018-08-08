var url = new URL(window.location.href);
var param = '?' + url.searchParams.toString();

$('#top-profile-loader').addClass('-show');
$.getJSON('/top-profiles' + param, function(data) {
  var topProfiles = $('.js-top-profiles');

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
  $('#top-profile-loader').removeClass('-show');
});
