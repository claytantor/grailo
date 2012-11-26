
/* needs to be in a class */

function encryptPassword(handle,publicKey) {
        var cypher = cryptico.encrypt(handle, publicKey).cipher;
        $('#id_pw_encrypted').val(cypher);
}

function generateUser(PassPhrase) {
    return $.Deferred(function( dfd ){

        var rsakey = cryptico.generateRSAKey(PassPhrase, 1024);

        var publicKeyString = cryptico.publicKeyString(rsakey);

        var model = {
            pu:publicKeyString
        };

        $('#keygen_result').html(Mustache.render(
            '<h4>User Public Key</h4> <span class="label">Will be saved on server.</span>'+
                '<textarea rows="4" wrap="hard" style="width:100%;" id="public_key">{{pu}}</textarea>'
            ,model));

        $('#gen_result_area').fadeIn( 1000, dfd.resolve );

    }).promise();
}

function getUsername(){
    return $.get('uname.json');
}

function decryptMessageHandler(event,ui) {
    var message_img_clicked = event.data.message_img_clicked;


    if($('#private_key').val()){
        $('#errors_area').html('');

        var cipherText = $(this).data('message-encrypted');

        var rsaKey = cryptico.generateRSAKey($('#private_key').val(), 1024);
        var decryptionResult = cryptico.decrypt(cipherText, rsaKey);
        $(this).siblings('.message').find('.message_text').html(decryptionResult.plaintext);

        $(message_img_clicked).find('img').attr("src",event.data.unlock_img);
        $(message_img_clicked).unbind('click');


    } else {
        $('#errors_area').html('<div class="alert alert-error"><h4>Please enter the feed private key.</h4></div>');
        $('#errors_area').show();
    }

    return false;
}

function replyMessageHandler(event,ui) {
    var message_reply_clicked = event.data.message_reply_clicked;
    var model = {};
    $(message_reply_clicked).parent().siblings('.message_reply_form').html(
        Mustache.render('<div><span class="label">Will be saved on server as encrypted text.</span>' +
            '<textarea rows="4" wrap="hard" style="width:100%;" id="message_unencrypted" ' +
            'placeholder="Enter reply..."></textarea><br><a href="" class="btn btn-primary">Save reply</a></div>',model));
    return false;
}

function loadCanvas(canvasName, dataURL) {
    var canvas = document.getElementById(canvasName);
    var context = canvas.getContext('2d');

    // load image from data url
    var imageObj = new Image();
    imageObj.onload = function() {
        context.drawImage(this, 0, 0);
    };

    imageObj.src = dataURL;
}


if (!window.GRAILO_Util) {
    window.GRAILO_Util = {
        env: {
            init: function(){

            },
            initJQuery: function(){
                if (typeof(jQuery.fn.parseJSON) == "undefined" || typeof(jQuery.parseJSON) != "function") {

                    //extensions, this is because prior to 1.4 there was no parse json function
                    jQuery.extend({
                        parseJSON: function( data ) {
                            if ( typeof data !== "string" || !data ) {
                                return null;
                            }
                            data = jQuery.trim( data );
                            if ( /^[\],:{}\s]*$/.test(data.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@")
                                .replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]")
                                .replace(/(?:^|:|,)(?:\s*\[)+/g, "")) ) {
                                return window.JSON && window.JSON.parse ?
                                    window.JSON.parse( data ) :
                                    (new Function("return " + data))();
                            } else {
                                jQuery.error( "Invalid JSON: " + data );
                            }
                        }
                    });
                }
            }
        },
        ui: {
            //{"errors":[{"errorMessage":"Please provide the name for your site.","errorCode":104}]}
            getErrorString: function(errors){
                var errorString = '';
                $(errors).each(function(i,item){
                    errorString = errorString+(i+1)+'. '+item.errorMessage+' ';
                });
                return errorString;
            },
            setStatus : function(statusArea, message, type, showloading){
                var _instance  = this;

                jQuery(statusArea).html('');
                jQuery(statusArea).removeClass();
                jQuery(statusArea).addClass(type);

                if(showloading){
                    jQuery(statusArea).append(showloading);
                }

                jQuery(statusArea).append('<em>'+message+'</em>');

                if(message != ''){
                    jQuery(statusArea).show();
                } else {
                    jQuery(statusArea).hide();
                }

            }
        },
        util: {
            remove :function(list, val) {
                list.splice(list.indexOf(val), 1);
            },
            listContains :function(list, val) {
                for ( var int = 0; int < list.length; int++) {
                    if(list[int] == val)
                        return true;
                }
                return false;
            },
            makeSet :function(list) {
                var set = {};
                for (var i = 0; i < list.length; i++)
                    set[list[i]] = true;
                list = [];
                for (var item in set)
                    list.push(item);
                return list;
            },
            log: function(logString){
                if (window.console) console.log(logString);
            },
            serialize: function(obj, prefix) {
                var str = [];
                for(var p in obj) {
                    var k = prefix ? prefix + "[" + p + "]" : p, v = obj[p];
                    str.push(typeof v == "object" ?
                        serialize(v, k) :
                        encodeURIComponent(k) + "=" + encodeURIComponent(v));
                }
                return str.join("&");
            },
            hashCode: function(val){
                var hash = 0;
                if (val.length == 0) return hash;
                for (i = 0; i < val.length; i++) {
                    char = val.charCodeAt(i);
                    hash = ((hash<<5)-hash)+char;
                    hash = hash & hash;
                }
                return hash;
            },
            trim: function (str) {
                return GRAILO_Util.util.ltrim(GRAILO_Util.util.rtrim(str), ' ');
            },
            ltrim: function (str) {
                return str.replace(new RegExp("^[" + ' ' + "]+", "g"), "");
            },
            rtrim: function (str) {
                return str.replace(new RegExp("[" + ' ' + "]+$", "g"), "");
            },
            preload: function(arrayOfImages) {
                jQuery(arrayOfImages).each(function(){
                    jQuery('<img/>')[0].src = this;
                });
            },
            update: function() {
                var obj = arguments[0], i = 1, len=arguments.length, attr;
                for (; i<len; i++) {
                    for (attr in arguments[i]) {
                        obj[attr] = arguments[i][attr];
                    }
                }
                return obj;
            },
            escape: function(s) {
                return ((s == null) ? '' : s)
                    .toString()
                    .replace(/[<>"&\\]/g, function(s) {
                        switch(s) {
                            case '<': return '&lt;';
                            case '>': return '&gt;';
                            case '"': return '\"';
                            case '&': return '&amp;';
                            case '\\': return '\\\\';
                            default: return s;
                        }
                    });
            },
            unescape: function (unsafe) {
                return unsafe
                    .replace(/&amp;/g, "&")
                    .replace(/&lt;/g, "<")
                    .replace(/&gt;/g, ">")
                    .replace(/&quot;/g, '"')
                    .replace(/&#039;/g, "'");
            },
            notundef: function(a, b) {
                return typeof(a) == 'undefined' ? b : a;
            },
            guidGenerator: function() {
                return (GRAILO_Util.util.S4()+GRAILO_Util.util.S4()+"-"+
                    GRAILO_Util.util.S4()+"-"+GRAILO_Util.util.S4()+"-"+
                    GRAILO_Util.util.S4()+"-"+
                    GRAILO_Util.util.S4()+GRAILO_Util.util.S4()+GRAILO_Util.util.S4());
            },
            keyGenerator: function() {
                return (GRAILO_Util.util.S4()+GRAILO_Util.util.S4());
            },
            tokenGenerator: function() {
                return (GRAILO_Util.util.S4()+GRAILO_Util.util.S4()+
                    GRAILO_Util.util.S4()+GRAILO_Util.util.S4()+
                    GRAILO_Util.util.S4()+
                    GRAILO_Util.util.S4()+GRAILO_Util.util.S4()+GRAILO_Util.util.S4());
            },
            S4: function() {
                return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
            },
            replaceAll: function(txt, replace, with_this) {
                return txt.replace(new RegExp(replace, 'g'),with_this);
            },
            startsWith: function(sourceString, startsWith) {
                return sourceString.indexOf(startsWith) == 0;
            },
            urlify: function(text) {
                var urlRegex = /(https?:\/\/[^\s]+)/g;
                return text.replace(urlRegex, function(url) {
                    return '<a href="' + url + '">' + url + '</a>';
                });
            },
            getParameter: function ( queryString, parameterName ) {
                // Add "=" to the parameter name (i.e. parameterName=value)
                var parameterName = parameterName + "=";
                if ( queryString.length > 0 ) {
                    // Find the beginning of the string
                    begin = queryString.indexOf ( parameterName );
                    // If the parameter name is not found, skip it, otherwise return the value
                    if ( begin != -1 ) {
                        // Add the length (integer) to the beginning
                        begin += parameterName.length;
                        // Multiple parameters are separated by the "&" sign
                        end = queryString.indexOf ( "&" , begin );
                        if ( end == -1 ) {
                            end = queryString.length
                        }
                        // Return the string
                        return unescape ( queryString.substring ( begin, end ) );
                    }
                    // Return "null" if no parameter has been found
                    return "null";
                }
            },
            getParameterByName: function (locationSearch, name)
            {
                name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
                var regexS = "[\\?&]" + name + "=([^&#]*)";
                var regex = new RegExp(regexS);
                var results = regex.exec(locationSearch);
                if(results == null)
                    return "";
                else
                    return decodeURIComponent(results[1].replace(/\+/g, " "));
            }
        }
    };
}
