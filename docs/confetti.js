'use strict';

let from = (function () {
    var toStr = Object.prototype.toString;
    var isCallable = function (fn) {
      return typeof fn === 'function' || toStr.call(fn) === '[object Function]';
    };
    var toInteger = function (value) {
      var number = Number(value);
      if (isNaN(number)) { return 0; }
      if (number === 0 || !isFinite(number)) { return number; }
      return (number > 0 ? 1 : -1) * Math.floor(Math.abs(number));
    };
    var maxSafeInteger = Math.pow(2, 53) - 1;
    var toLength = function (value) {
      var len = toInteger(value);
      return Math.min(Math.max(len, 0), maxSafeInteger);
    };

    // The length property of the from method is 1.
    return function from(arrayLike/*, mapFn, thisArg */) {
      // 1. Let C be the this value.
      var C = this;

      // 2. Let items be ToObject(arrayLike).
      var items = Object(arrayLike);

      // 3. ReturnIfAbrupt(items).
      if (arrayLike == null) {
        throw new TypeError("Array.from requires an array-like object - not null or undefined");
      }

      // 4. If mapfn is undefined, then let mapping be false.
      var mapFn = arguments.length > 1 ? arguments[1] : void undefined;
      var T;
      if (typeof mapFn !== 'undefined') {
        // 5. else
        // 5. a If IsCallable(mapfn) is false, throw a TypeError exception.
        if (!isCallable(mapFn)) {
          throw new TypeError('Array.from: when provided, the second argument must be a function');
        }

        // 5. b. If thisArg was supplied, let T be thisArg; else let T be undefined.
        if (arguments.length > 2) {
          T = arguments[2];
        }
      }

      // 10. Let lenValue be Get(items, "length").
      // 11. Let len be ToLength(lenValue).
      var len = toLength(items.length);

      // 13. If IsConstructor(C) is true, then
      // 13. a. Let A be the result of calling the [[Construct]] internal method of C with an argument list containing the single item len.
      // 14. a. Else, Let A be ArrayCreate(len).
      var A = isCallable(C) ? Object(new C(len)) : new Array(len);

      // 16. Let k be 0.
      var k = 0;
      // 17. Repeat, while k < len… (also steps a - h)
      var kValue;
      while (k < len) {
        kValue = items[k];
        if (mapFn) {
          A[k] = typeof T === 'undefined' ? mapFn(kValue, k) : mapFn.call(T, kValue, k);
        } else {
          A[k] = kValue;
        }
        k += 1;
      }
      // 18. Let putStatus be Put(A, "length", len, true).
      A.length = len;
      // 20. Return A.
      return A;
    };
  }());

// Converted from https://github.com/daniel-lundin/dom-confetti

var defaultColors = ['#a864fd', '#29cdff', '#78ff44', '#ff718d', '#fdff6a'];

var confetti = function () {
    function createElements(root, elementCount, colors) {
      return from({ length: elementCount }).map(function (_, index) {
        var element = document.createElement('div');
        var color = colors[index % colors.length];
        element.style['background-color'] = color; // eslint-disable-line space-infix-ops
        element.style.width = '10px';
        element.style.height = '10px';
        element.style.position = 'absolute';
        element.style.zIndex = '900';
        root.appendChild(element);
        return element;
      });
    }

    function randomPhysics(angle, spread, startVelocity) {
      var radAngle = angle * (Math.PI / 180);
      var radSpread = spread * (Math.PI / 180);
      return {
        x: 0,
        y: 0,
        wobble: Math.random() * 10,
        velocity: startVelocity * 0.5 + Math.random() * startVelocity,
        angle2D: -radAngle + (0.5 * radSpread - Math.random() * radSpread),
        angle3D: -(Math.PI / 4) + Math.random() * (Math.PI / 2),
        tiltAngle: Math.random() * Math.PI
      };
    }

    function updateFetti(fetti, progress, decay) {
      /* eslint-disable no-param-reassign */
      fetti.physics.x += Math.cos(fetti.physics.angle2D) * fetti.physics.velocity;
      fetti.physics.y += Math.sin(fetti.physics.angle2D) * fetti.physics.velocity;
      fetti.physics.z += Math.sin(fetti.physics.angle3D) * fetti.physics.velocity;
      fetti.physics.wobble += 0.1;
      fetti.physics.velocity *= decay;
      fetti.physics.y += 3;
      fetti.physics.tiltAngle += 0.1;

      var _fetti$physics = fetti.physics,
          x = _fetti$physics.x,
          y = _fetti$physics.y,
          tiltAngle = _fetti$physics.tiltAngle,
          wobble = _fetti$physics.wobble;

      var wobbleX = x + 10 * Math.cos(wobble);
      var wobbleY = y + 10 * Math.sin(wobble);
      var transform = 'translate3d(' + wobbleX + 'px, ' + wobbleY + 'px, 0) rotate3d(1, 1, 1, ' + tiltAngle + 'rad)';

      fetti.element.style.transform = transform;
      fetti.element.style.opacity = 1 - progress;

      /* eslint-enable */
    }

    function animate(root, fettis, decay) {
      var totalTicks = 200;
      var tick = 0;

      function update() {
        fettis.forEach(function (fetti) {
          return updateFetti(fetti, tick / totalTicks, decay);
        });

        tick += 1;
        if (tick < totalTicks) {
          requestAnimationFrame(update);
        } else {
          fettis.forEach(function (fetti) {
            return root.removeChild(fetti.element);
          });
        }
      }

      requestAnimationFrame(update);
    }

    function confetti(root) {
      var _ref = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {},
          _ref$angle = _ref.angle,
          angle = _ref$angle === undefined ? 90 : _ref$angle,
          _ref$decay = _ref.decay,
          decay = _ref$decay === undefined ? 0.9 : _ref$decay,
          _ref$spread = _ref.spread,
          spread = _ref$spread === undefined ? 45 : _ref$spread,
          _ref$startVelocity = _ref.startVelocity,
          startVelocity = _ref$startVelocity === undefined ? 45 : _ref$startVelocity,
          _ref$elementCount = _ref.elementCount,
          elementCount = _ref$elementCount === undefined ? 50 : _ref$elementCount,
          _ref$colors = _ref.colors,
          colors = _ref$colors === undefined ? defaultColors : _ref$colors;

      var elements = createElements(root, elementCount, colors);
      var fettis = elements.map(function (element) {
        return {
          element: element,
          physics: randomPhysics(angle, spread, startVelocity)
        };
      });

      animate(root, fettis, decay);
    }

    return confetti
}()