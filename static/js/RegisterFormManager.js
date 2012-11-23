function GRAILO_RegisterFormManager (target,cfg) {
    this.target = target;
    var errors = this.initCfg(cfg);
    if(errors.length>0){
        $(target).append('<div>problem</div>');
    } else {
        this.init(target);
    }

    return this;
}

GRAILO_RegisterFormManager.prototype.initCfg = function( cfg ) {
    var errors = [];
    return errors;
};


GRAILO_RegisterFormManager.prototype.init = function( target ) {
    var _instance = this;
    var formArea = $('<div>form area</div>');
    $(target).append(formArea);
    executeTest(target,13,32);
};

