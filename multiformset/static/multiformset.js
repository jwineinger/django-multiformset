function multiformset( options ) {

    // Create some defaults, extending them with any options that were provided
    var settings = $.extend( {
        'template_selector' : '.form_template',
        'add_form_selector' : '#multiformset-add_form',
        'new_form_parent' : '#multiformset-new_forms',
        'template_value_attr': 'data-form-class',
        'template_text_attr': 'data-form-class'

    }, options);

    var $chooser = $(settings.add_form_selector);
    $(settings.template_selector).each(function(idx, el) {
        var $el = $(el);
            $chooser.append($("<option></option>")
                .attr("value", $el.attr(settings.template_value_attr))
                .text($el.attr(settings.template_text_attr)));
    });
    $(settings.add_form_selector).click(function(evt) {
        // don't submit if this input happens to be within the form
        evt.preventDefault();

        // update total form count
        var form_name = $chooser.val();
        var $total_forms = $("#id_" + form_name + "-TOTAL_FORMS");
        var qty = parseInt($total_forms.val());
        $total_forms.val(qty + 1);

        // copy the template and replace prefixes with the correct index
        var html = $("#" + form_name + "-form_template").clone().html().replace(/__prefix__/g, qty);
        $(settings.new_form_parent).append(html);
    });

}