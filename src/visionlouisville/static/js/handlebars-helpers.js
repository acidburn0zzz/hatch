/*globals Handlebars $ _ moment */

var VisionLouisville = VisionLouisville || {};

(function(NS) {
  Handlebars.registerHelper('authenticated', function(options) {
    return !!NS.currentUserData ? options.fn(this) : options.inverse(this);
  });

  Handlebars.registerHelper('if_supported', function(options) {
    var userId, supportingIDs;
    
    if (!NS.currentUserData) return options.inverse(this);

    userId = NS.currentUserData['id'],
    supportingIds = _.pluck(this.supporters, 'id');
    return _.contains(supportingIds, userId) ? options.fn(this) : options.inverse(this);
  });

  Handlebars.registerHelper('STATIC_URL', function() {
    return NS.staticURL;
  });

  Handlebars.registerHelper('LOGIN_URL', function(redirectTo, options) {
    if (arguments.length === 1) {
      options = redirectTo;
      redirectTo = undefined;
    }
    return NS.getLoginUrl(redirectTo);
  });

  Handlebars.registerHelper('category_prompt', function(category) {
    return NS.Config.categories[category].prompt;
  });

  Handlebars.registerHelper('window_location', function() {
    return window.location.toString();
  });

  // usage: {{pluralize collection.length 'quiz' 'quizzes'}}
  Handlebars.registerHelper('pluralize', function(number, single, plural) {
    return (number === 1) ? single : plural;
  });

  Handlebars.registerHelper('fromnow', function(datetime) {
    if (datetime) {
      return moment(datetime).fromNow();
    }
    return '';
  });

  Handlebars.registerHelper('formatdatetime', function(datetime, format) {
    if (datetime) {
      return moment(datetime).format(format);
    }
    return '';
  });

  Handlebars.registerHelper('select', function(value, options) {
    var $el = $('<div/>').html(options.fn(this)),
      selectValue = function(v) {
        $el.find('[value="'+v+'"]').attr({
          checked: 'checked',
          selected: 'selected'
        });
      };

    if (_.isArray(value)) {
      _.each(value, selectValue);
    } else {
      selectValue(value);
    }

    return $el.html();
  });

}(VisionLouisville));