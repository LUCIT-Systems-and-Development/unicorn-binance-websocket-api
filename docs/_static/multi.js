// Make multiple variants of a sections dynamically switchable.
//
// A multi-variant section is created by using nested .. container::
// directives as follows:
//
// .. container:: NAME-multi
//
//    .. container:: NAME-python
//
//       CONTENT
//
//    .. container:: NAME-cpp
//
//       CONTENT
//
//    MORE-VARIANTS
//
// The "multi" string is mandatory. NAME and the -python, -cpp,
// etc. suffixes are arbitrary.

function getParam(name, fallback) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if (results == null)
        return fallback;
    else
        return results[1];
}

function switchMulti(parent, all, switchTo) {
  jQuery.map(all, function (name) {
      node = $('.' + parent + '-multi').find('.' + name);
      if (name === switchTo) {
          node.slideDown();
      } else {
          node.slideUp();
      }
  });
}

function getScriptDirectory(name) {
    var scripts = document.getElementsByTagName('script');
    for (i = 0; i < scripts.length; i++) {
        if (scripts[i].src.indexOf(name) > -1) {
            var path = scripts[i].src;
            path = path.substring(0, path.lastIndexOf("/") + 1);
            return path;
        }
    }
}

$(document).ready(function () {
    var directory = getScriptDirectory("multi.js");
    jQuery.map($('*[class*="multi"]').filter('*[class*="container"]'), function (parent) {
        //
        var parentName = parent.className.replace(/^(.*)-multi .*container$/, '$1');
        var all = jQuery.map($(parent)
                             .find('*[class*="container"]')
                             .filter('*[class*="' + parentName + '"]'),
                             function (node) {
                                 var clazz = node.className;
                                 return {
                                     'name':  clazz.replace(new RegExp('^.*(' + parentName + '-[^ ]+) .*$'),
                                                            '$1'),
                                     'label': clazz.replace(new RegExp('^.*' + parentName + '-([^ ]+) .*$'),
                                                            '$1')
                                 };
                             });
        var allNames = jQuery.map(all, function (nameAndLabel) { return nameAndLabel.name; });

        var code = jQuery.map(all, function (nameAndLabel) {
            return '<a href="javascript:switchMulti(\''
                + parentName + '\', ['
                + (jQuery
                   .map(allNames, function (name) { return '\'' + name + '\''; })
                   .join(', '))
                + '], \''
                + nameAndLabel.name + '\')">' + nameAndLabel.label + '</a>';
        }).join('&nbsp;|&nbsp;');
        $(parent).prepend('<div class="switcher"><img class="switchicon" alt="" src="'
                          + directory
                          + '/multiswitch.svg"/>Show '
                          + code
                          + '</div>');

        parent.className += ' multi';
        var defaultName = getParam(parentName, allNames[0]);
        switchMulti(parentName, allNames, defaultName);
    });
});
