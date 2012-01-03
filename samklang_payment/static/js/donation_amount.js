var removeSelected = function() {
    $$("p.active").each(function(e) {
        e.removeClass("active");
    });
};

window.addEvent('domready', function() {

    $$("p.alt").each(function(el) {
        el.addEvent('click', function() {
            val = el.get('text');
            document.id('id_amount').set('value', val);
            removeSelected();
            el.addClass("active");

        });
    });

    document.id('id_amount').addEvent("keydown", function() {
        removeSelected();
    });

});
