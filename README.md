grailo
======

A python and Django secure feed based social network using public/private key encryption. The client
side is responsible for generating and managing keys. The server is the transport and stores encrypted data.

#Important Links#
The following projects heavily influenced this project and may have code included in Grailo. Please give props.
We stand on the sholders of giants.

* [cryptico](https://github.com/claytantor/cryptico) - Javascript public/private key encryption.
* [django-icanhaz ](https://github.com/carljm/django-icanhaz) - Mustache.js template fixes

#Interesting Articles#
The following articles have influenced decisions we have made and we think are interesting.
* [Atsushi Oka Titanium Core](http://ats.oka.nu/titaniumcore/js/crypto/readme.txt)
* [Simple Authentication Backend](http://www.djangorocks.com/tutorials/creating-a-custom-authentication-backend/creating-a-simple-authentication-backend.html)
* [django-microblogging](https://github.com/skabber/django-microblogging/tree/master/microblogging) - simple microblogging
* [django-friends](https://github.com/jtauber/django-friends) - friendship, contact and invitation management for the Django web framework

#Things we do before we commit

1. $ pip freeze > requirements.txt
2. update example settings