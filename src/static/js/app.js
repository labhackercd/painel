var text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean bibendum erat ac justo sollicitudin, quis lacinia ligula fringilla. Pellentesque hendrerit, nisi vitae posuere condimentum, lectus urna accumsan libero, rutrum commodo mi lacus pretium erat. Phasellus pretium ultrices mi sed semper. Praesent ut tristique magna. Donec nisl tellus, sagittis ut tempus sit amet, consectetur eget erat. Sed ornare gravida lacinia. Curabitur iaculis metus purus, eget pretium est laoreet ut. Quisque tristique augue ac eros malesuada, vitae facilisis mauris sollicitudin. Mauris ac molestie nulla, vitae facilisis quam. Curabitur placerat ornare sem, in mattis purus posuere eget. Praesent non condimentum odio. Nunc aliquet, odio nec auctor congue, sapien justo dictum massa, nec fermentum massa sapien non tellus. Praesent luctus eros et nunc pretium hendrerit. In consequat et eros nec interdum. Ut neque dui, maximus id elit ac, consequat pretium tellus. Nullam vel accumsan lorem.';
var lines = text.split(/[,. ]+/g),
  data = Highcharts.reduce(lines, function (arr, word) {
    var obj = Highcharts.find(arr, function (obj) {
      return obj.name === word;
    });
    if (obj) {
      obj.weight += 1;
    } else {
      obj = {
        name: word,
        weight: 1
      };
      arr.push(obj);
    }
    return arr;
  }, []);


var archimedeanSpiral = function archimedeanSpiral(t) {
    t *= 0.1;
    return {
        x: t * Math.cos(t),
        y: t * Math.sin(t)
    };
};

Highcharts.seriesTypes.wordcloud.prototype.spirals.archimedean = archimedeanSpiral;

var randomPlacement = function randomPlacement(point, options) {
  var field = options.field,
    r = options.rotation;
  return {
    x: getRandomPosition(field.width) - (field.width / 2),
    y: getRandomPosition(field.height) - (field.height / 2),
   rotation: getRotation(r.orientations, r.from, r.to)
  };
};
Highcharts.seriesTypes.wordcloud.prototype.placementStrategy.random= randomPlacement;

Highcharts.chart('wordcloud-container', {
    plotOptions: {
        series: {
            cursor: 'pointer',
            point: {
                events: {
                    click: function () {
                        console.log(this)
                    }
                }
            }
        }
    },

  series: [{
    type: 'wordcloud',
    spiral: 'rectangular',
    placementStrategy: 'center',
    rotation: {
      from: 0,
      to: 0
    },
    data: data,
    name: 'Occurrences'
  }],
  title: {
    text: ''
  }
});