(function( $ ){
    $.fn.registerForm = function( cfg ) {
        return this.each(function() {

            var $this = $(this);
            $this.cfg = cfg;

            $this.registerFormManager = new GRAILO_RegisterFormManager(this,cfg);


        });
    };

})( jQuery );