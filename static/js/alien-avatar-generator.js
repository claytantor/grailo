// Canvas
var px = 30,
    px_s = 15;

// Generate
var generate = $('button[role="generate"]');
generate.click(function(e) {
    Canvas.newAvatar();
});

Canvas = {
    el : {
        dom : $('#random_avatar').get(0),
        jq : null,
        img : null
    },
    ctx : null,
    size : {
        width : 300,
        height: 300
    },

    init : function() {
        this.el.jq = $(this.el.dom);
        this.el.img = $('img[role="result"]');

        if (this.el.dom.getContext) {
            this.ctx = this.el.dom.getContext('2d');

            this.el.jq.attr('width', this.size.width);
            this.el.jq.attr('height', this.size.height);

            this.el.img.css('width', this.size.width);
            this.el.img.css('height', this.size.height);

            this.newAvatar();
        } else {
            // Not supported
        }
    },

    newAvatar : function() {
        // Background gradient
        var cxlg = this.ctx.createLinearGradient(0, 0, 300, 300);
        cxlg.addColorStop(0, '#555');
        cxlg.addColorStop(0.5, '#ccc');
        cxlg.addColorStop(1.0, '#666');
        this.ctx.fillStyle = cxlg;

        this.ctx.fillRect(0,0,300,300);
        this.ctx.fillRect(300,0,300,300);
        this.ctx.fillRect(0,300,300,300);

        // Face
        face();

        // Eyes
        eyes();

        // Mouth
        mouth();

        // Hair
        hair();

        // Body
        body();

        this.toImg();

    },

    toImg : function() {
        $('#img_alien_avatar').hide();
        var img_src = this.el.dom.toDataURL("image/png"),
            old_img = this.el.img,
            new_img = this.el.img.clone(true);

        this.el.img.before(new_img);

        // Warp up old img only if there is a old img
        if (old_img.attr('src') != undefined) {
            old_img.addClass('goaway');

            setTimeout(function() {
                old_img.remove();
                $('#img_alien_avatar').show();
            }, 400);
        } else {
            old_img.remove();
        }

        this.el.img = $(new_img);
        this.el.img.attr('src', img_src);

    }
}

Canvas.init();

/**
 * Face
 */
function face() {
    var faces = [
        [ // F@ face
            [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3.5],
            [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4],
            [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5],
            [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 5.5]
        ],
        [ // Normal face
            [3, 3], [4, 3], [5, 3], [6, 3],
            [3, 4], [4, 4], [5, 4], [6, 4],
            [3, 5], [4, 5], [5, 5], [6, 5],
            [3, 6], [4, 6], [5, 6]
        ],
        [ // Alien face
            [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3],
            [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4],
            [3, 5], [4, 5], [5, 5], [6, 5],
            [3, 6], [4, 6], [5, 6]
        ]
    ];

    // Face
    draw(
        randomColor(),
        faces[randomBetween(faces.length)]
    );
}

/**
 * Eyes
 */
function eyes() {
    var eyes = [
        [
            [4, 4], [6, 4]
        ]
    ]

    // Eyes
    draw(randomColor(), eyes[randomBetween(eyes.length)]);

    var pupil = [
        [[4.5, 4], [6.5, 4]],
        [[4.5, 4.5], [6.5, 4.5]],
        [[4, 4.5], [6, 4.5]],
        [[4, 4], [6.5, 4.5]],
        [[4.5, 4.5], [6, 4]],
        []
    ];

    // Pupil
    draw(
        randomColor(),
        pupil[randomBetween(pupil.length)],
        px_s
    );
}

function mouth() {
    // Mouth
    var mouths = [
        [[4, 6], [5, 6]]
    ];

    draw(
        randomColor(),
        mouths[randomBetween(mouths.length)]
    );

    // Decorations
    var decorations = [
        [[5, 6]],
        [[4, 6], [4.5, 6.5], [5, 6], [5.5, 6.5]],
        []
    ];

    draw(
        randomColor(),
        decorations[randomBetween(decorations.length)],
        px_s
    );
}

/**
 * Hair
 */
function hair() {
    var hair = [
        [
            [4, .5], [5, .5], [6,0],
            [3, 1.5], [4, 1],  [5, 1], [6, 1],
            [3, 2.5], [4, 2],  [5, 2], [6, 2]
        ],
        [
            [4, .5], [5, .5],[6,0],[7,0],
            [2, 1.5],[3, 1.5], [4, 1],  [5, 1], [6, 1],
            [2, 2.5], [3, 2.5], [4, 2],  [5, 2], [6, 2], [7, 2]
        ],
        [
            [4, .5], [5, .5],
            [2, 1.5],[3, 1.5], [4, 1.5],  [5, 1.5], [6, 1.5], [7, 1.5],
            [1, 2.5],[2, 2.5], [3, 2.5], [4, 2.5],  [5, 2.5], [6, 2.5], [7, 2.5], [8, 2.5]
        ],
        [
            [2, .5], [7, .5],
            [2, 1.5], [3, 2], [4, 1.5], [5, 1.5], [6, 2], [7, 1.5],
            [2, 2.5], [4, 2.5],  [5, 2.5], [7, 2.5]
        ],
        []
    ];

    draw(
        randomColor(),
        hair[randomBetween(hair.length)]
    );
}

/**
 * Body
 */
function body() {
    var bodys = [
        [
            [2, 7], [3, 7], [4, 7], [5, 7], [6, 7],
            [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8],
            [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9]
        ],
        [
            [2, 7], [3, 7], [4, 7], [5, 7], [5, 7], [6, 7], [7, 7],
            [0, 8], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8],
            [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9]
        ]
    ];

    // Body
    draw(randomColor(), bodys[randomBetween(bodys.length)]);

    // Decorations
    var body_decorations = [
        [ // Tie
            [3, 7], [5, 7],
            [4, 8],
            [4, 9]
        ],
        []
    ];

    draw(
        randomColor(),
        body_decorations[randomBetween(body_decorations.length)]
    );

    // Decorations 2
    var body_decorations_2 = [
        [
            [3.5, 7.5], [5, 7], [5, 7],
            [4, 8],
            [4, 9]
        ],
        [
            [3, 8.5], [5.5, 8.5],
            [2.5, 9], [6, 9],
            [2.5, 9.5], [5.5, 9.5]
        ]
    ];

    draw(
        randomColor(),
        body_decorations_2[randomBetween(body_decorations_2.length)],
        px_s
    );
}

/**
 * Draw something.
 */
function draw(color, coords, size) {
    $.each(coords, function(i, v) {

        var _size = px;

        if (size != undefined) {
            _size = size;
        }

        Canvas.ctx.fillStyle = color;
        Canvas.ctx.fillRect(coords[i][0] * px, coords[i][1] * px, _size, _size);
    });
}

/**
 * Return a random value not greater than max.
 */
function randomBetween(max) {
    var r;
    do {r = Math.random();} while(r == 1.0);
    return parseInt(r * max);
}

/*
 * Return a random color as hex.
 */
function randomColor() {
    Math.seedrandom();
    var vla = '#' + Math.floor(Math.random()*16777215).toString(16);
    return vla;
}

// seedrandom.js version 2.0.
// Author: David Bau 4/2/2011
//
// Defines a method Math.seedrandom() that, when called, substitutes
// an explicitly seeded RC4-based algorithm for Math.random().  Also
// supports automatic seeding from local or network sources of entropy.
//
// Usage:
//
//   <script src=http://davidbau.com/encode/seedrandom-min.js></script>
//
//   Math.seedrandom('yipee'); Sets Math.random to a function that is
//                             initialized using the given explicit seed.
//
//   Math.seedrandom();        Sets Math.random to a function that is
//                             seeded using the current time, dom state,
//                             and other accumulated local entropy.
//                             The generated seed string is returned.
//
//   Math.seedrandom('yowza', true);
//                             Seeds using the given explicit seed mixed
//                             together with accumulated entropy.
//
//   <script src="http://bit.ly/srandom-512"></script>
//                             Seeds using physical random bits downloaded
//                             from random.org.
//
//   <script src="https://jsonlib.appspot.com/urandom?callback=Math.seedrandom">
//   </script>                 Seeds using urandom bits from call.jsonlib.com,
//                             which is faster than random.org.
//
// Examples:
//
//   Math.seedrandom("hello");            // Use "hello" as the seed.
//   document.write(Math.random());       // Always 0.5463663768140734
//   document.write(Math.random());       // Always 0.43973793770592234
//   var rng1 = Math.random;              // Remember the current prng.
//
//   var autoseed = Math.seedrandom();    // New prng with an automatic seed.
//   document.write(Math.random());       // Pretty much unpredictable.
//
//   Math.random = rng1;                  // Continue "hello" prng sequence.
//   document.write(Math.random());       // Always 0.554769432473455
//
//   Math.seedrandom(autoseed);           // Restart at the previous seed.
//   document.write(Math.random());       // Repeat the 'unpredictable' value.
//
// Notes:
//
// Each time seedrandom('arg') is called, entropy from the passed seed
// is accumulated in a pool to help generate future seeds for the
// zero-argument form of Math.seedrandom, so entropy can be injected over
// time by calling seedrandom with explicit data repeatedly.
//
// On speed - This javascript implementation of Math.random() is about
// 3-10x slower than the built-in Math.random() because it is not native
// code, but this is typically fast enough anyway.  Seeding is more expensive,
// especially if you use auto-seeding.  Some details (timings on Chrome 4):
//
// Our Math.random()            - avg less than 0.002 milliseconds per call
// seedrandom('explicit')       - avg less than 0.5 milliseconds per call
// seedrandom('explicit', true) - avg less than 2 milliseconds per call
// seedrandom()                 - avg about 38 milliseconds per call
//
// LICENSE (BSD):
//
// Copyright 2010 David Bau, all rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//   1. Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//   2. Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
//
//   3. Neither the name of this module nor the names of its contributors may
//      be used to endorse or promote products derived from this software
//      without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
/**
 * All code is in an anonymous closure to keep the global namespace clean.
 *
 * @param {number=} overflow
 * @param {number=} startdenom
 */
(function (pool, math, width, chunks, significance, overflow, startdenom) {


//
// seedrandom()
// This is the seedrandom function described above.
//
    math['seedrandom'] = function seedrandom(seed, use_entropy) {
        var key = [];
        var arc4;

        // Flatten the seed string or build one from local entropy if needed.
        seed = mixkey(flatten(
            use_entropy ? [seed, pool] :
                arguments.length ? seed :
                    [new Date().getTime(), pool, window], 3), key);

        // Use the seed to initialize an ARC4 generator.
        arc4 = new ARC4(key);

        // Mix the randomness into accumulated entropy.
        mixkey(arc4.S, pool);

        // Override Math.random

        // This function returns a random double in [0, 1) that contains
        // randomness in every bit of the mantissa of the IEEE 754 value.

        math['random'] = function random() {  // Closure to return a random double:
            var n = arc4.g(chunks);             // Start with a numerator n < 2 ^ 48
            var d = startdenom;                 //   and denominator d = 2 ^ 48.
            var x = 0;                          //   and no 'extra last byte'.
            while (n < significance) {          // Fill up all significant digits by
                n = (n + x) * width;              //   shifting numerator and
                d *= width;                       //   denominator and generating a
                x = arc4.g(1);                    //   new least-significant-byte.
            }
            while (n >= overflow) {             // To avoid rounding up, before adding
                n /= 2;                           //   last byte, shift everything
                d /= 2;                           //   right using integer math until
                x >>>= 1;                         //   we have exactly the desired bits.
            }
            return (n + x) / d;                 // Form the number within [0, 1).
        };

        // Return the seed that was used
        return seed;
    };

//
// ARC4
//
// An ARC4 implementation.  The constructor takes a key in the form of
// an array of at most (width) integers that should be 0 <= x < (width).
//
// The g(count) method returns a pseudorandom integer that concatenates
// the next (count) outputs from ARC4.  Its return value is a number x
// that is in the range 0 <= x < (width ^ count).
//
    /** @constructor */
    function ARC4(key) {
        var t, u, me = this, keylen = key.length;
        var i = 0, j = me.i = me.j = me.m = 0;
        me.S = [];
        me.c = [];

        // The empty key [] is treated as [0].
        if (!keylen) { key = [keylen++]; }

        // Set up S using the standard key scheduling algorithm.
        while (i < width) { me.S[i] = i++; }
        for (i = 0; i < width; i++) {
            t = me.S[i];
            j = lowbits(j + t + key[i % keylen]);
            u = me.S[j];
            me.S[i] = u;
            me.S[j] = t;
        }

        // The "g" method returns the next (count) outputs as one number.
        me.g = function getnext(count) {
            var s = me.S;
            var i = lowbits(me.i + 1); var t = s[i];
            var j = lowbits(me.j + t); var u = s[j];
            s[i] = u;
            s[j] = t;
            var r = s[lowbits(t + u)];
            while (--count) {
                i = lowbits(i + 1); t = s[i];
                j = lowbits(j + t); u = s[j];
                s[i] = u;
                s[j] = t;
                r = r * width + s[lowbits(t + u)];
            }
            me.i = i;
            me.j = j;
            return r;
        };
        // For robust unpredictability discard an initial batch of values.
        // See http://www.rsa.com/rsalabs/node.asp?id=2009
        me.g(width);
    }

//
// flatten()
// Converts an object tree to nested arrays of strings.
//
    /** @param {Object=} result
     * @param {string=} prop
     * @param {string=} typ */
    function flatten(obj, depth, result, prop, typ) {
        result = [];
        typ = typeof(obj);
        if (depth && typ == 'object') {
            for (prop in obj) {
                if (prop.indexOf('S') < 5) {    // Avoid FF3 bug (local/sessionStorage)
                    try { result.push(flatten(obj[prop], depth - 1)); } catch (e) {}
                }
            }
        }
        return (result.length ? result : obj + (typ != 'string' ? '\0' : ''));
    }

//
// mixkey()
// Mixes a string seed into a key that is an array of integers, and
// returns a shortened string seed that is equivalent to the result key.
//
    /** @param {number=} smear
     * @param {number=} j */
    function mixkey(seed, key, smear, j) {
        seed += '';                         // Ensure the seed is a string
        smear = 0;
        for (j = 0; j < seed.length; j++) {
            key[lowbits(j)] =
                lowbits((smear ^= key[lowbits(j)] * 19) + seed.charCodeAt(j));
        }
        seed = '';
        for (j in key) { seed += String.fromCharCode(key[j]); }
        return seed;
    }

//
// lowbits()
// A quick "n mod width" for width a power of 2.
//
    function lowbits(n) { return n & (width - 1); }

//
// The following constants are related to IEEE 754 limits.
//
    startdenom = math.pow(width, chunks);
    significance = math.pow(2, significance);
    overflow = significance * 2;

//
// When seedrandom.js is loaded, we immediately mix a few bits
// from the built-in RNG into the entropy pool.  Because we do
// not want to intefere with determinstic PRNG state later,
// seedrandom will not call math.random on its own again after
// initialization.
//
    mixkey(math.random(), pool);

// End anonymous scope, and pass initial values.
})(
    [],   // pool: entropy pool starts empty
    Math, // math: package containing random, pow, and seedrandom
    256,  // width: each RC4 output is 0 <= x < 256
    6,    // chunks: at least six RC4 outputs for each double
    52    // significance: there are 52 significant digits in a double
);