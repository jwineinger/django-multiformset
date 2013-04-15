$(function() {
    var $chooser = $('#multiformset-form_chooser');
    $(".form_template").each(function(idx, el) {
        var $el = $(el);
            $chooser.append($("<option></option>")
                .attr("value", $el.attr('data-form-class'))
                .text($el.attr('data-form-class')));
    });
    $("#multiformset-add_form").click(function() {
        // update total form count
        var form_name = $chooser.val();
        var $total_forms = $("#id_" + form_name + "-TOTAL_FORMS");
        var qty = parseInt($total_forms.val());
        $total_forms.val(qty + 1);

        // copy the template and replace prefixes with the correct index
        var html = $("#" + form_name + "-form_template").clone().html().replace(/__prefix__/g, qty);
        $("#multiformset-new_forms").append(html);
    });
});